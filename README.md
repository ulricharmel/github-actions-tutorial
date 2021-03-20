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
The above code example would totally work, but in large programs, this is just not feasible. 