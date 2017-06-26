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
and will raise a MaxRetriesPerformed error if all of the retrys fail.


times
    Retry a certain number of times

    >>> @rever(times=10)

    *Explanation: retry 10 times, pauses for 0 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail*

pause
    Pause for some number of seconds between each retry

    >>> @rever(pause=5)

    *Explanation: retry 1 time, pauses for 5 seconds between each retry,
    catch any exception, raise MaxRetriesPerformed if all attempts fail*


exception
    Catch one specific exception

    >>> @rever(exception=TypeError)
    >>> @rever(exception=(TypeError, ))

    *Explanation: retry 1 time, pauses for 0 seconds between each retry,
    catch TypeError, raise MaxRetriesPerformed if all attempts fail*

    Catch one of multiple specific exceptions

    >>> @rever(exception=(TypeError, ConnectionError))

    *Explanation: retry 1 time, pauses for 0 seconds between each retry,
    catch TypeError or ConnectionError, raise MaxRetriesPerformed if all attempts fail*

raises
    Raise an exception or do not

    >>> @rever(raises=False)

    *Explanation: retry 1 time, pauses for 0 seconds between each retry,
    catch any exception, do not raise MaxRetriesPerformed if all attempts fail*


Installation
------------

If you want to install it via pip, try this in the terminal:

    pip install rever

Or this:

    pip install git+git://github.com/limecrayon/rever


Next Steps
----------

1)  Create a keyword argument to rever which will enable you to call a function prior to retrying.

    >>> def reset_switch():
    >>>     function_to_deactivate_switch()
    >>>     function_to_reactivate_switch()

    >>> @rever(prior=reset_switch)
    >>> def enjoy_lightbulb(args, kwargs):
    >>>     some_activity(args, kwargs)
