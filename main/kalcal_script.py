from kalcal.filters import ekf
from kalcal.smoothers import eks
from kalcal.tools.utils import gains_vector
from kalcal.generation import parser
from kalcal.generation import from_ms
from kalcal.generation import create_ms
from kalcal.generation import loader
from kalcal.plotting.multiplot import plot_time

import matplotlib.pyplot as plt
import numpy as np
from os import path


def main():   
    # Get configurations from yaml
    yaml_args = parser.yaml_parser('config.yml')
    cms_args = yaml_args['create_ms']
    fms_args = yaml_args['from_ms'] 
    
    # If new ms is made, run `from_ms`
    new_ms = False

    # Create measurement set
    if path.isdir(cms_args.msname):
        s = input(f"==> `{cms_args.msname}` exists, "\
                + "continue with `create_ms`? (y/n) ")
        
        if s == 'y':
            create_ms.new(cms_args) 
            new_ms = True
    else:
        create_ms.new(cms_args)  
        new_ms = True
    
    # Generate jones and data
    if path.isfile(fms_args.out) and not new_ms:
        s = input(f"==> `{fms_args.out}` exists, "\
                + "continue with `generate`? (y/n) ")
        
        if s == 'y':
            from_ms.both(fms_args) 
    else:
        from_ms.both(fms_args) 

    # Load ms and gains data
    tbin_indices, tbin_counts, ant1, ant2,\
            vis, model, weight, jones = loader.get(fms_args)    

    #Get dimension values
    n_time, n_ant, n_chan, n_dir = jones.shape    
    
    # Set parameters for process and measurement noise
    sigma_f = 1.0
    sigma_n = 0.5

    # Select extended kalman filter and smoother algorithms
    ext_kalman_filter = ekf.numpy_algorithm
    ext_kalman_smoother = eks.numpy_algorithm

    # Set random seed
    np.random.seed(666)

    # Create prior state vector
    mp = np.ones((n_ant, n_chan, n_dir, 2), dtype=np.complex128)
    mp = gains_vector(mp)  

    # Create prior covariance matrix
    Pp = np.eye(mp.size, dtype=np.complex128)

    # Process noise matrix
    Q = sigma_f**2 * np.eye(mp.size, dtype=np.complex128)

    # Measurement noise matrix
    R = 2 * sigma_n**2 * np.eye(n_ant * (n_ant - 1) * n_chan, 
                                    dtype=np.complex128) 
    
    # Run EKF
    m, P = ext_kalman_filter(mp, Pp, model, vis, weight, Q, R, 
                                ant1, ant2, tbin_indices, tbin_counts)

    # Run EKS - 3 times
    ms, Ps, _ = ext_kalman_smoother(m, P, Q)
    ms, Ps, _ = ext_kalman_smoother(ms[::-1], Ps[::-1], Q)
    ms, Ps, _ = ext_kalman_smoother(ms[::-1], Ps[::-1], Q)

    # Plot results for antennas 1 to 3, with 0 as reference
    print("==> Finished - creating plots")
    plot_time(
        jones, 'True Jones', '-',
        m, 'EKF', '+',
        ms, 'EKS', '--',
        title='KALCAL: NUMPY|JIT Algorithms',
        show=[1, 2, 3]
    )
    
    plt.show()

    # Done
    print("==> Done.")


if __name__ == "__main__":
    main()