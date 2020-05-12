---------------------------
Rever, A retrying decorator
---------------------------

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

    >>> from rever import rever
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

Installation
------------

::

    $ pip install rever



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

**default**
    Default behavior

    >>> @rever()

    - rever will use exponential backoff
    - rever will have a total pause time of 30 seconds (total time your function will pause)
    - rever will have 10 steps (steps here means the number of times your function will retry)
    - rever will catch any exception
    - rever will ultimately raise an exception if all retrys fail

**exception**
    Catch one specific exception

    >>> @rever(exception=TypeError)
    >>> @rever(exception=(TypeError, ))

    - rever will use exponential backoff
    - rever will have a total pause time of 30 seconds (total time your function will pause)
    - rever will have 10 steps (steps here means the number of times your function will retry)
    - rever will catch only *TypeError*
    - rever will ultimately raise an exception if all retrys fail

    Catch one of multiple specific exceptions

    >>> @rever(exception=(TypeError, ConnectionError))

    - rever will use exponential backoff
    - rever will have a total pause time of 30 seconds (total time your function will pause)
    - rever will have 10 steps (steps here means the number of times your function will retry)
    - rever will catch any of only *TypeError* or *ConnectionError*
    - rever will ultimately raise an exception if all retrys fail

raises
    Raise an exception or do not

    >>> @rever(raises=False)

    - rever will use exponential backoff
    - rever will have a total pause time of 30 seconds (total time your function will pause)
    - rever will have 10 steps (steps here means the number of times your function will retry)
    - rever will catch any exception
    - rever will ultimately *not* raise an exception if all retrys fail

prior
    Call a function prior to retrying

    >>> @rever(prior=some_function_to_call_prior_to_retyring)

    - rever will use exponential backoff
    - rever will have a total pause time of 30 seconds (total time your function will pause)
    - rever will have 10 steps (steps here means the number of times your function will retry)
    - rever will catch any exception
    - rever will ultimately raise an exception if all retrys fail
    - *rever will call some function prior to each retry*

**Below used only if backoff is set to False, it is included for backwards compatibility**

times
    Retry a certain number of times

    >>> @rever(backoff=False, times=10)

    - rever will *not* use exponential backoff
    - rever will have a total pause time of *0* seconds (total time your function will pause)
    - rever will retry *1* time (time here means the number of times your function will retry)
    - rever will catch any exception
    - rever will ultimately raise an exception if all retrys fail

pause
    Pause for some number of seconds between each retry

    >>> @rever(backoff=False, pause=5)

    - rever will *not* use exponential backoff
    - rever will have a total pause time of *5* seconds (total time your function will pause)
    - rever will retry *1* time (time here means the number of times your function will retry)
    - rever will catch any exception
    - rever will ultimately raise an exception if all retrys fail


You can basically use any combination of keywords you would like

Testing
-------

To run tests, clone the github repository:

    $ git clone https://github.com/liamcryan/rever
    $ cd rever
    $ pip install pytest
    $ pytest
