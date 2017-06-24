---------------------------
Rever, A retrying decorator
---------------------------

Explanation
-----------

A retry decorator can be useful when you are scraping web pages.  A GET request is not always successful
the first time, and if you are scraping many sites, your program could bug out.  For example:

>>> urls = [url1, url2, url3, ...., url9999]
>>> responses = [get_website(url) for url in urls]

If any of the calls to get_website fail, then you can't really get all your responses...

>>> import requests  # if you are using requests...
>>> from rever import rever
>>> @rever()
>>> def get_website_bad_connection(website):
>>>     return requests.get(website)


Keyword Arguments
-----------------

The rever decorator takes only keyword arguments.  By default, if no kwargs are supplied, then
the decorator will retry the function 1 time, with a 1 second pause, and catch any exception that occurs.


times
    Retry a certain number of times

    >>> @rever(times=10)

pause
    Pause for some number of seconds

    >>> @rever(pause=5)

exception
    Catching one exception

    >>> @rever(exception=TypeError)
    >>> @rever(exception=(TypeError, ))

    Catching multiple exceptions:

    >>> @rever(exception=(TypeError, ConnectionError))


Putting it all together
    >>> @rever(times=5, pause=2, exception=(ConnectionError,))


Installation
------------

This is a very small amount of code and you can copy and paste the decorator into your project.

If you want to install it via pip, this might work:

>>> pip install git+git://github.com/limecrayon/rever
