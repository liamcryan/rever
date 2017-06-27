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

The rever decorator takes only keyword arguments.  By default, if no kwargs are supplied, then
the decorator will retry the function 1 time, with a 0 second pause, catch any exception that occurs,
raise a MaxRetriesPerformed error if all of the retrys fail, and will not call any function prior to retrying.


times
    Retry a certain number of times

    >>> @rever(times=10)

    *Explanation: retry 10 times, pause for 0 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail,
    do not call any function prior to retrying*

pause
    Pause for some number of seconds between each retry

    >>> @rever(pause=5)

    *Explanation: retry 1 time, pause for 5 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail,
    do not call ny function prior to retrying*


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


Installation
------------

If you want to install it via pip, you can install from PyPI:

    $ pip install rever


Testing
-------

To run tests, clone the github repository:

    $ git clone https://github.com/limecrayon/rever

If you want to use tox, in the terminal type:

    $ pip install tox

    $ tox

Or you could skip tox and use pytest:

    $ pip install pytest

    $ python -m pytest


Next Steps
----------

This has only been tested on Python 3.5.  It will probably work on other Python 3.x version as well.
Next step is to test on other Python versions, possibly using Travis CI.