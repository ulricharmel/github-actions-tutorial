# GitHub Actions Tutorial

## 1. Introduction
This tutorial serves as a quick introduction into concepts like *tests* and *continuous* integration to enable you to utilize GitHub's very own CI environment, *GitHub Actions*.

## 2. Unit Tests in `python`

### 2.1 Unit Test Framework 
This is a necessity for the longevity of any software project. As the number of lines of code grow, the ability for you to account for errors and possible bugs diminishes, because we are only human. However, we need to spot these issues one way or another before it causes any fatal software meltdown, patch them and re-release the program. This may sound like a daunting task, sinc it is intractable to all spot problems with our code we might not even know exists? Fortunately, it can easily be done with the use of a *Unit Test Framework*. But before we move to this, we need to start with the concept of *Unit Tests*.

**What is a unit test framework and how are they used?**: 
>"Simply stated, they are software tools to support writing and running unit tests, including a foundation on which to build tests and the functionality to execute the tests and report their results.They are not solely tools for testing; they can also be used as development tools on apar with preprocessors and debuggers. Unit test frameworks can contribute to almost every stage of software development, including software architecture and design, code implementation and debugging, performance optimization, and quality assurance."
>
> **\- pg. 5, Paul Hamill. 2004. *Unit test frameworks* (First. ed.). O'Reilly.**

<hr style="height:5px;border-width:0;background-color:#e6e6e6">

### 2.2 Unit Tests
A *unit test* is a single case or scenario we wish to check for possibe bugs or errors in our code. For each issue that can be realised, we can create a unit test for it. So, lets begin with an example issue. Look at the function `create_profile` below:
```python 
def create_profile(firstname, lastname, age, email, location):
    """ Create a dictionary with information about 
    a given person."""

    profile = {
        "firstname" : firstname,
        "lastname"  : lastname,
        "age"       : age,
        "email"     : email,
        "location"  : location
    }

    return profile
```
It creates a dictionary containing information about a person and returns it. Now, call it with some random string inputs (Here I am referencing [Malfurion](https://wow.gamepedia.com/Malfurion_Stormrage) from the [Warcraft Universe](https://wow.gamepedia.com/Wowpedia)):
```python 
profile = create_profile(
            firstname="Malfurion", 
            lastname="Stormrage", 
            age="15032", 
            email="druids.ftw@gmail.com", 
            location="Suramar, Broken Isles")
```
Then print our new `profile` dictionary:
```python 
print(profile)
> {'firstname': 'Malfurion', 'lastname': 'Stormrage', 'age': '15032', 'email': 'druids.ftw@gmail.com', 'location': 'Suramar, Broken Isles'}

```
and *hey presto*! It works just fine. We can try another example:
```python 
profile = create_profile(
            firstname=__import__("this"), 
            lastname=hex(0xDEADC0DE), 
            age="https://theuselessweb.com/", 
            email=10**1000,
            location=None)
```
which has the print output of:
```python 
print(profile)
>The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    {'firstname': <module 'this' from '/usr/lib/python3.6/this.py'>, 'lastname':    '0xDEADC0DE', 'age': 'https://theuselessweb.com/', 'email':    1000000000000000000000000000000000000000000000000000000000000000000000000000000    0000000000000000000000000000000000000000000000000000000000000000000000000000000 0000000000000000000000000000000000000000000000000000000000000000000000000000000  0000000000000000000000000000000000000000000000000000000000000000000000000000000   0000000000000000000000000000000000000000000000000000000000000000000000000000000    0000000000000000000000000000000000000000000000000000000000000000000000000000000 0000000000000000000000000000000000000000000000000000000000000000000000000000000  0000000000000000000000000000000000000000000000000000000000000000000000000000000   0000000000000000000000000000000000000000000000000000000000000000000000000000000    0000000000000000000000000000000000000000000000000000000000000000000000000000000 0000000000000000000000000000000000000000000000000000000000000000000000000000000  0000000000000000000000000000000000000000000000000000000000000000000000000000000   00000000000000000000000000000000000000000000000000000, 'location': None}
```
which is also perfectly fine obviously, since it *ran*. However, this was not the intended purpose of `create_profile` when desiging it and nor were we expecting inputs like that. But it is still a possibility that these unsavoury events can occur, so we have to somehow check for bugs like this to fix any holes in our code! This is where *unit tests* come in. 

First lets begin with the defintion of our function:
`"""Create a dictionary with information about a given person."""`

So it takes various information about the person as inputs. Lets list them and write what we expect from each input:

Argument | Data Type | Conditions
--- | --- | --- 
`firstname`, `lastname` | `string` | Contains only letters characters and some punctuation
`age` | `integer` | Greater than 0 (i.e. positive)
`email` | `string` | Formatted with an @ sign and domain, e.g. .com
`location` | `string` | A list of locations separated by commas

With this clear baseline, we can develop some simple tests to check that this function meets these conditions. One way we can do this is to run the function with a couple of input cases we know *should* and *shouldn't* be valid and see if the function continues with or rejects the inputs, respectively. For this example, I will only show the test case for the `firstname`:
```python 
def test_firstname():
    """Unit test for input `firstname` of `create_profile`. Prints test outcome
    for each input."""

    # Passed tests counter
    counter = 0

    # List of correct inputs
    correct_inputs = ["Brian", "Cyril", "Thatcher", "Kel'Thuzad"]

    # Test correct inputs
    for INPUT in correct_inputs:
        # If INPUT is correct, we continue
        try:
            create_profile(
                firstname=INPUT,        # The input we are testing
                lastname="lastname",    # Fill others with known correct values
                age=50,
                email="email@domain.com",
                location="Street, City, Country"
            )

            # Test passed for input
            print(f"PASSED for valid `firstname={INPUT}` in `create_profile`")
            counter += 1
        except:
            # Test failed for input
            print(f"FAILED for valid `firstname={INPUT}` in `create_profile`")

    # List of incorrect inputs
    incorrect_inputs = [1234, "1234", "&.&.&.&", __import__("numpy")]

    # Test incorrect inputs
    for INPUT in incorrect_inputs:
        # If INPUT is incorrect, we continue
        try:
            create_profile(
                firstname=INPUT,        # The input we are testing
                lastname="lastname",    # Fill others with known correct values
                age=50,
                email="email@domain.com",
                location="Street, City, Country"
            )
            
            # Test failed for input
            print(f"FAILED for invalid `firstname={INPUT}` in `create_profile`")
        except:
            # Test passed for input
            print(f"PASSED for invalid `firstname={INPUT}` in `create_profile`")
            counter += 1

    # Output total passed tests
    print(f"TOTAL PASSED: {counter}/8 ({round(counter/8.0*100, 2)}%)")
```
The first half of he function tests valid inputs, whilst the second half tests for invalid inputs. The tests centre around if the function raises an error or not. To run this test, call `test_firstname` in the same script, and analyze the output:
```bash
PASSED for valid `firstname=Brian` in `create_profile`
PASSED for valid `firstname=Cyril` in `create_profile`
PASSED for valid `firstname=Thatcher` in `create_profile`
PASSED for valid `firstname=Kel'Thuzad` in `create_profile`
FAILED for invalid `firstname=1234` in `create_profile`
FAILED for invalid `firstname=1234` in `create_profile`
FAILED for invalid `firstname=&.&.&.&` in `create_profile`
FAILED for invalid `firstname=<module 'numpy' from '/home/brian/.local/lib/python3.6/site-packages/numpy/__init__.py'>` in `create_profile`
TOTAL PASSED: 4/8 (50.0%)
```
Great! We can clearly see our function works for valid inputs, but completely fails on invalid inputs. From here, make the necessary changes to ensure the code is how we intended it to be and that all tests pass! 

<hr style="height:5px;border-width:0;background-color:#e6e6e6">

### 2.3 Automating Unit Tests
The above code example would totally work, but in large programs, this is not feasible for the amount of things we would need to test for. Luckily, this is where unit testing frameworks come in. They automate the boring stuff and leave us to only write the necessary tests.

In `python`, these frameworks come in the form of packages. The native one that comes with `python` is `unittest` (see [link](https://docs.python.org/3/library/unittest.html)). However, there are plenty of external unit testing libraries out there ([list](https://blog.testproject.io/2020/10/27/top-python-testing-frameworks/)), but for this tutorial, I will use `pytest`. It is my personal preference for testing for the following reasons:

* Tests are simply designed
* Can run in parallel with `xdist` plugin
* Lots of guides, documentation and technical support
* Super easy to parameterize test inputs

Once we have setup our testing framework, all we need to do is call it whenever we make a change to our code, and the framework will systematically go through all your tests to see if any error has occured and if something has broken because of your change.

This back-and-forth between writing code, then testing, then fixing any errors that come from it, is the basic idea behind *Test-driven Software Development*. We start with an expectation of what our program should do, we create tests to make sure these requirements are met, then we write the code that satisfies these tests, and in doing so, creates an error-free and well-developed software. 

In our specific case in radio-interferometry, we predominantly work with `python` as our coding platform and so in the next section, I will demonstrate simply how to achieve the above in `python`, utilizing `pytest`.

<hr style="height:5px;border-width:0;background-color:#e6e6e6">

## 2.4 Using `pytest`
Looking at our previous example, lets develop a unit test with `pytest` for the `age` input. We begin by importing the package:
```python 
import pytest
```
And thats it. When we do this, `pytest` will handle the rest. Now we just need to make a test. Make sure the function that is doing the test has the prefix `test_` so that `pytest` can identify it and run it. As a start, write a simple test that always passes:
```python 
def test_age():
    """Unit test for input `age` of `create_profile`."""

    assert True
``` 
Here I've utilized the keyword function `assert`, which is a built-in function that takes a boolean (true or false) expression. If the input is `True`, do *nothing*. Else if the input is `False`, then raise an `AssertionError`. It is simple, but powerful in terms of testing. Tests written with `pytest` predominantly would use `assert` to see if a test has passed or failed. The above code runs `assert True` which will *always* pass, no matter what. To see this, run the command:
```bash
pytest -v <filepath>
```

where `<filepath>` is the path to your script with the test in it. Again, my script is called `script.py`, so *my* `pytest` output is:
```bash
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.6.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/brian/Code/github-actions-tutorial
plugins: benchmark-3.2.3, forked-1.3.0, xdist-2.2.1
collected 1 item                                                                                                                                                                                                  

script.py::test_age PASSED                                                                                                                                                                                  [100%]

================================================================================================ 1 passed in 0.02s ================================================================================================
```
The `-v` option lists each test as it runs. As we can see, our test was found and it passed. Time to develop the test further. A `pytest` test function will fail if an error is thrown, so we can write a simple test as follows:
```python 
def test_age():
    """Unit test for input `age` of `create_profile`."""

    # List of correct inputs
    correct_inputs = [1, 42, 1001, 2021]

    # Test correct inputs
    for INPUT in correct_inputs:
        # Pytest will fail if function raises an error       
        create_profile(
            firstname="firstname", 
            lastname="lastname",
            age=INPUT,
            email="email@domain.com",
            location="Street, City, Country"
        )

    # List of incorrect inputs
    incorrect_inputs = [-1, "hello", str, __import__("numpy")]

    # Test incorrect inputs
    for INPUT in incorrect_inputs:
        # Pytest will fail if function doesn't raise an error
        with pytest.raises(Exception) as e:
            create_profile(
                firstname="firstname",
                lastname="lastname",
                age=INPUT,
                email="email@domain.com",
                location="Street, City, Country"
            )
```
This adaptation does not use `assert` function, since we are checking for errors raised. Noting the context manager function `pytest.raises`: the test will pass if an error *is* raised, and fail if *nothing* happens. Using the `pytest` command as before, we see that indeed our test fails:
```bash
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.6.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/brian/Code/github-actions-tutorial
plugins: benchmark-3.2.3, forked-1.3.0, xdist-2.2.1
collected 1 item                                                                                                                                                                                                  

script.py F                                                                                                                                                                                                 [100%]

==================================================================================================== FAILURES =====================================================================================================
____________________________________________________________________________________________________ test_age _____________________________________________________________________________________________________

    def test_age():
        """Unit test for input `age` of `create_profile`."""
    
        # List of correct inputs
        correct_inputs = [1, 42, 1001, 2021]
    
        # Test correct inputs
        for INPUT in correct_inputs:
            # Pytest will fail if function raises an error
            create_profile(
                firstname="firstname",
                lastname="lastname",
                age=INPUT,
                email="email@domain.com",
                location="Street, City, Country"
            )
    
        # List of incorrect inputs
        incorrect_inputs = [-1, "hello", str, __import__("numpy")]
    
        # Test incorrect inputs
        for INPUT in incorrect_inputs:
            # Pytest will fail if function doesn't raise an error
            with pytest.raises(Exception) as e:
                create_profile(
                    firstname="firstname",
                    lastname="Lastname",
                    age=INPUT,
                    email="email@domain.com",
>                   location="Street, City, Country"
                )
E               Failed: DID NOT RAISE <class 'Exception'>

script.py:48: Failed
============================================================================================= short test summary info =============================================================================================
FAILED script.py::test_age - Failed: DID NOT RAISE <class 'Exception'>
================================================================================================ 1 failed in 0.24s ================================================================================================
```
Browsing over the `pytest`-output, we see it failed because the function did not raise an error for the invalid inputs. I prefer to use `assert` functions, so here is an approach to `test_age` that does uses them:
```python 
def test_age(args):
    """Unit test for input `age` of `create_profile`."""

    # INPUT is the value, EXPECTED is the expected result of the test using INPUT
    INPUT, EXPECTED = args

    # Initial OUTCOME of the test
    OUTCOME = False

    try:
        # Run the function with INPUT
        create_profile(*INPUT)

        # Function finished with no error
        OUTCOME = True

    except:
        # Function failed with an error
        pass

    # Now test if our OUTCOME matches the EXPECTED outcome
    assert OUTCOME == EXPECTED    
```
> "The `*` in `*INPUT` is an unpacking operator. It allows grouped values in a `tuple` or `list` to be distributed, in order, over the function arguments."

This is quite different from the previous and won't work straight away. The most notabe reason for this is that there are no inputs yet. There is only an argument called `args` and we use it to get variables `INPUT` and `EXPECTED`. To provide inputs, we are going to use a `python` wrapper called `pytest.fixture`. 

`pytest.fixture` is placed on functions we want `pytest` to evaluate before it begins testing. The most common use for this is creating session-wide inputs for all tests. An example of this for our case would be the following (to apply a wrapper, we use the `@` symbol):
```python 
@pytest.fixture
def args():
    """Provide `INPUT` and `EXPECTED` for `test_age`"""

    # Inputs for `create_profile`
    INPUT = ("firstname", "lastname", 42, 
                "email@domain.com", "Street, City, Country")
    
    # Expected output
    EXPECTED = True

    # Return arguments
    return INPUT, EXPECTED
```
Now when we begin testing, this function is executed and returned to all tests that call it as an argument. Place this code above the function `test_age` and now we can run `pytest`, again, using the same command as before. The test should now pass as per values in `args`:
```bash
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.6.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/brian/Code/github-actions-tutorial
plugins: benchmark-3.2.3, forked-1.3.0, xdist-2.2.1
collected 1 item                                                                                                                                                                                                  

script.py .                                                                                                                                                                                                 [100%]

================================================================================================ 1 passed in 0.02s ================================================================================================
```
We can take this one step further and parametrize it! I will create two lists of ages just below my imports: *correct ages* and *incorrect ages*. Each element is a `tuple` that consists of the `INPUT` and the corresponding `EXPECTED` result based on if `INPUT` is valid or invalid.
```python 
# Integers 0 to 999
CORRECT_AGES = [(i, True) for i in range(10**3)]

# Integers -1 to -999
INCORRECT_AGES = [(-i, False) for i in range(1, 10**3)]

# Concatenate inputs
AGES = CORRECT_AGES + INCORRECT_AGES
```
Next we add an argument to `pytest.fixture` and change `args` as follows:
```python 
@pytest.fixture(params=AGES)
def args(request):
    """Provide `INPUT` and `EXPECTED` for `test_age`"""

    # Unpack param
    AGE, EXPECTED = request.param

    # Inputs for `create_profile`
    INPUT = ("firstname", "lastname", AGE, 
                "email@domain.com", "Street, City, Country")

    # Return arguments
    return INPUT, EXPECTED
```
The `params` argument will indicate to `pytest` that we need to parametrize, and to access each value, we call `request.param`. Now each value in `AGES` will create an individual test, listing each as it progresses. This allows for more insightful testing and for combinations of inputs as well. After running `pytest` again, the last few lines of the output will be:
```bash
...
FAILED script.py::test_age[args1993] - assert True == False
FAILED script.py::test_age[args1994] - assert True == False
FAILED script.py::test_age[args1995] - assert True == False
FAILED script.py::test_age[args1996] - assert True == False
FAILED script.py::test_age[args1997] - assert True == False
FAILED script.py::test_age[args1998] - assert True == False
======================================================================================== 999 failed, 1000 passed in 8.89s =========================================================================================
```
Which is what we expected:

1. Integers 0 to 999 (1000 cases) should pass the test
2. Integers -1 to -999 (999 cases) should fail the test

This is excellent! Now, if we wish to add more inputs to test, we just need to append it to `AGES`. This concludes the basic usage of `pytest` for this tutorial.

<hr style="height:5px;border-width:0;background-color:#e6e6e6">

### 2.5 Getting to grips with unit testing and `pytest`
I have done a very simple and crude guide on unit testing in `python` for the needs of this tutorial, and so do not take my test designs as standard, since every project has its own requirements and restrictions. Look through the documentation and figure out what works for you! If you want to learn more, here is a list of resources and guides to help explain these concepts in an in-depth manner:

* [Unit Tests in Python || Python Tutorial || Learn Python Programming, *by Socratica* (YouTube)](https://www.youtube.com/watch?v=1Lfv5tUGsn8)
* [Python Testing Cookbook, *by Greg Turnquist* (Textbook)](https://edu.heibai.org/Python_Testing_Cookbook.pdf)
* [Testing python applications with pytest, *by SEMAPHORE* (Article)](https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest)
* [Python Testing with pytest, *by Brian Okken (2017)* (Textbook)](http://library.sadjad.ac.ir/opac/temp/18467.pdf)
* [pytestguide.readthedocs.io (Website)](https://pytestguide.readthedocs.io/en/latest/)

<hr style="height:10px;border-width:0;background-color:#e6e6e6">

## 3. Continuous Integration