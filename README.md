# GitHub Actions Tutorial
---
## 1. Introduction
This tutorial serves as a quick introduction into concepts like *tests* and *continuous* integration to enable you to utilize GitHub's very own CI environment, *GitHub Actions*.

## 2. Unit Tests in `python`
### 2.1 Unit Test Framework 
This is a necessity for the longevity of any software project. As the number of lines of code grow, the ability for you to account for errors and possible bugs diminishes, because we are only human. However, we need to spot these issues one way or another before it causes any fatal software meltdown. We can achieve this by using an *Unit Test Framework*.

**What is a unit test framework and how are they used?**: 
>"Simply stated, they are software tools to support writing and running unit tests, including a foundation on which to build tests and the functionality to execute the tests and report their results.They are not solely tools for testing; they can also be used as development tools on apar with preprocessors and debuggers. Unit test frameworks can contribute to almost every stage of software development, including software architecture and design, code implementation and debugging, performance optimization, and quality assurance."
>
> **\- pg. 5, Paul Hamill. 2004. *Unit test frameworks* (First. ed.). O'Reilly.**

### 2.2 Unit Tests
A *unit test* is a single case or scenario we wish to check for possibe bugs or errors in our code. Take for example the function `create_profile` below:
```[python]
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
Call the function with some random string inputs (Here I am referencing [Malfurion](https://wow.gamepedia.com/Malfurion_Stormrage) from the [Warcraft Universe](https://wow.gamepedia.com/Wowpedia)):
```[python]
profile = create_profile(
            firstname="Malfurion", 
            lastname="Stormrage", 
            age="15032", 
            email="druids.ftw@gmail.com", 
            location="Suramar, Broken Isles")
```
Then print our new `profile`:
```[python]
print(profile)
> {'firstname': 'Malfurion', 'lastname': 'Stormrage', 'age': '15032', 'email': 'druids.ftw@gmail.com', 'location': 'Suramar, Broken Isles'}

```
and *hey presto*! It works just fine. We can try another example:
```[python]
profile = create_profile(
            firstname=__import__("this"), 
            lastname=hex(0xDEADC0DE), 
            age="https://theuselessweb.com/", 
            email=10**1000,
            location=None)
```
with print output of:
```[python]
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
which is also perfectly fine, since it *ran*. Obviously, this was not the intended purpose of the function and nor were we expecting inputs like that. But it is still a possibility as we just saw, so we have to somehow check for a bug like this. This is where *unit tests* come in. 

First lets begin with the defintion of our function:
`""" Create a dictionary with information about a given person."""`

Which takes various information about the person as inputs. Lets list them and list what we expect from each input:

Argument | Data Type | Conditions
--- | --- | --- 
`firstname`, `lastname` | `string` | Contains only letters characters and some punctuation
`age` | `integer` | Greater than 0 (i.e. positive)
`email` | `string` | Formatted with an @ sign and domain, e.g. .com
`location` | `string` | A list of locations separated by commas

So we can develop some simple tests to check for these conditions. One way we can do this is to run the function with a couple of input cases we know should and shouldn't be allowed and see if the function rejects it. For this example, I will only show the case for the first input:
```[python]
def test_firstname():
    """Unit test for input `firstname` of `create_profile`. If
    the test passes, return True. Else if it fails, return False."""

    # List of correct inputs
    correct_inputs = ["Brian", "Cyril", "Thatcher", "Kel'Thuzad"]

    # Test correct inputs
    for INPUT in correct_inputs:
        # If INPUT is correct, we continue
        try:
            create_profile(
                firstname=INPUT,        # The input we are testing
                lastname="Lastname",    # Fill others with known correct values
                age=50,
                email="email@domain.com",
                location="Street, City, Country"
            )
        except:

            # Test failed for input
            return False

    # List of incorrect inputs
    incorrect_inputs = [1234, "1234", "&.&.&.&", __import__("numpy")]

    # Test incorrect inputs
    for INPUT in incorrect_inputs:
        # If INPUT is incorrect, we continue
        try:
            create_profile(
                firstname=INPUT,        # The input we are testing
                lastname="Lastname",    # Fill others with known correct values
                age=50,
                email="email@domain.com",
                location="Street, City, Country"
            )
            
            # Function did not raise error, so test failed
            return False
        except:
            pass

    # Else, all tests passed
    return True
```
Now run this with the `assert` keyword:
> "The `assert` function raises an error if the input is `False`, and does nothing if `True`."
```[python]
assert test_firstname()
```
Which gives us an `AssertionError`, which means our test *failed*. Now we know our code doesn't work as we wanted and we can make the necessary changes to ensure our code is how we intended and this test passes! 

## 2.3 Automating Unit Tests
The above code example would totally work, but in large programs, this is just not feasible for the amount of things we would need to test for. Luckily, this is where unit testing frameworks come in. They automate the boring stuff and leave us to write the necessary tests only.

In `python`, these frameworks come in the form of packages. The native one that comes with `python` is `unittest` (see [link](https://docs.python.org/3/library/unittest.html)). There are plenty of external unit testing libraries out there ([list](https://blog.testproject.io/2020/10/27/top-python-testing-frameworks/)), but for this tutorial, I will use `pytest`. The reasons for this choice are:

* Tests are simply designed
* Can run in parallel with `xdist` plugin
* Lots of technical support
* Fixtures allow for super-easy parameterizing

## 2.4 Using `pytest`
Looking at our previous example, lets develop a unit test for the `age` input. We begin by importing the package:
```[python]
import pytest
```
And thats it. When we do this, `pytest` will handle the rest. Now we just have to make a test. Make sure the function that is doing the test has the prefix `test_` so that `pytest` can identify it as a test. To begin with, we will write a simple test that just passes:
```[python]
def test_age():
    """Unit test for input `age` of `create_profile`."""

    assert True
``` 
In a terminal, run the command `pytest -v <filepath>` where `<filepath>` is the path to our script with the test in it. My script is called `script.py`, so **my** `pytest` output is:
```[bash]
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
The `-v` option lists each test as it runs. As we can see, our test was found and it passed. Now we can develop the test. Here is one similar to that of `test_firstname`:
```[python]
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
                location="Street, City, Country"
            )
```
This adaptation does not use `assert` functions, but rather it tries to run tests by checking if errors are raised. With `pytest.raises`, the test will pass if an error IS raised. Using the `pytest` command as before, we see that indeed our test fails:
```[bash]
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
As we can see, it failed because the function did not raise an error. Here is a different approach to `test_age` that does use the `assert` function:
```[python]
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
This is quite different from the previous and won't work straight away. The most notabe reason for this is that there are no inputs yet. However, we have an argument called `args` and we use it to get `INPUT` and `EXPECTED`. To provide inputs, we are going to use a `python` wrapper called `pytest.fixture`. 

`pytest.fixture` is placed on functions we want `pytest` to evaluate before we begin testing. The most common use for this is creating inputs. An example of this for our case would be the following (to apply a wrapper, we use the `@` symbol):
```[python]
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
Place this code above the function `test_age` and now we can run `pytest` again using the same command as before. The test should pass as per values in `args`:
```[bash]
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.6.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
benchmark: 3.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/brian/Code/github-actions-tutorial
plugins: benchmark-3.2.3, forked-1.3.0, xdist-2.2.1
collected 1 item                                                                                                                                                                                                  

script.py .                                                                                                                                                                                                 [100%]

================================================================================================ 1 passed in 0.02s ================================================================================================
```
Taking this one step further and parametrize this! I will create two lists of ages just below my imports: correct ages and incorrect ages.
```[python]
# Integers 0 to 999
CORRECT_AGES = [(i, True) for i in range(10**3)]

# Integers -1 to -999
INCORRECT_AGES = [(-i, False) for i in range(1, 10**3)]

# Concatenate inputs
AGES = CORRECT_AGES + INCORRECT_AGES
```
Next we add an argument to `pytest.fixture` and change `args` as follows:
```[python]
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
This will now create every age input listed in `AGES` and run it as an individual test, listing each parameter as it progresses. This allows for a more insightful test and allows for combinations of inputs as well. Here is what the output should look like:
```[bash]
```