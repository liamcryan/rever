---------------------------
Rever, A retrying decorator
---------------------------


Why use it?
-----------

A retry decorator can be useful in many situations.  One example is when scraping web pages.
Suppose you have a function that retrieves the status code response of a GET request.  If the status
code returns 200, then you are happy.  But if not, then there here is what you might do:

1)  You could write your retrying logic directly into your functions

    >>> def get_response(webpage):
    >>>     response = function_to_get_webpage(webpage)
    >>>     status_code = function_to_get_status_code(response)
    >>>     if status_code == 200:
    >>>         return status_code
    >>>     else:
    >>>         time.sleep(3)
    >>>         num_tries -= 1
    >>>         if num_tries > 0:
    >>>             return get_response(webpage)
    >>>
    >>> if __name__ == "__main__":
    >>>     num_tries = 2
    >>>     get_response("http://www.google.com")

2)  You could use a retrying decorator like rever

    >>> @rever(times=2, pause=3, exception=MyException, raises=False)
    >>> def get_response(webpage):
    >>>     response = function_to_get_webpage(webpage)
    >>>     status_code = function_to_get_status_code(response)
    >>>     if status_code == 200:
    >>>         return status_code
    >>>     else:
    >>>         raise MyException
    >>>
    >>> if __name__ == "__main__":
    >>>     get_response("http://www.google.com")


In the first example, you need to write out the retrying logic yourself.  The second
example it is taken care of in the decorator; a nice way of keeping things separate.


Keyword Arguments
-----------------

The rever decorator takes only keyword arguments.

Possible keyword arguments:

*backoff*:

    description:  if True subsequent pauses for each retry will increase exponentially
    possible values:  boolean

*total_pause*:

    description:  the total time you are willing to wait for all of your pauses between retrys
    possible values: integer or float

*steps*:

    description:  related to backoff and is set at 10 because wikipedia says so:  https://en.wikipedia.org/wiki/Exponential_backoff
    possible values:  integer

*exception*:

    description:   you can choose which exception or exceptions to catch
    possible values:  any Exception that gets raised by Python

*raises*:

    description:  if all the retrys fail, do you want to raise an exception or not?
    possible values:  boolean

*prior*:

    description:  if you want to call another function/script prior to retrying, you can do so but without any args or kwargs
    possible values:  a simple function...cannot take args or kwargs

**These arguments are used if *backoff* is set to False**:

*times*:

    description:  the number of times you want the function to retry
    possible values:  integer

*pause*:

    description:  the number of seconds you want to pause before your function retrys
    possible values:  integer or float


Examples & Explanation
----------------------

**This section needs to be updated**

exception
    Catch one specific exception

    >>> @rever(exception=TypeError)
    >>> @rever(exception=(TypeError, ))

    *Explanation: retry 1 time, pause for 0 seconds between each retry,
    catch TypeError, raise MaxRetriesPerformed if all attempts fail,
    do not call any function prior to retrying*

    Catch one of multiple specific exceptions

    >>> @rever(exception=(TypeError, ConnectionError))

    *Explanation: retry 1 time, pause for 0 seconds between each retry,
    catch TypeError or ConnectionError, raise MaxRetriesPerformed if all attempts fail,
    do not call any function prior to retrying*

raises
    Raise an exception or do not

    >>> @rever(raises=False)

    *Explanation: retry 1 time, pauses for 0 seconds between each retry,
    catch any exception, do not raise MaxRetriesPerformed if all attempts fail,
    do not call any function prior to retrying*

prior
    Call a function prior to retrying

    >>> @rever(prior=some_function_to_call_prior_to_retyring)

    *Explanation: retry 1 time, pause for 0 seconds between each retry,
    catch any exception, do not raise MaxRetriesPerformed if all attempts fail,
    call a function prior to retrying*


**Below used only if backoff is set to False**

times
    Retry a certain number of times

    >>> @rever(backoff=False, times=10)

    *Explanation: retry 10 times, pause for 0 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail,
    do not call any function prior to retrying*

pause
    Pause for some number of seconds between each retry

    >>> @rever(backoff=False, pause=5)

    *Explanation: retry 1 time, pause for 5 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail,
    do not call ny function prior to retrying*

Installation
------------

If you want to install it via pip, you can install from PyPI:

    $ pip install rever


Testing
-------

To run tests, clone the github repository:

    $ git clone https://github.com/limecrayon/rever


If you want to use tox, in the terminal type:

    $ cd rever

    $ pip install tox

    $ tox

Or you could skip tox and use pytest:

    $ pip install pytest

    $ python -m pytest


Next Steps
----------

This has only been tested on Python 3.5.  It will probably work on other Python 3.x version as well.
If you are using version other than 3.5 you will need to include your version in the tox.ini file when running tox.

I want to try out TravisCI at some point.

Examples section needs to be updated.
