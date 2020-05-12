-------
History
-------

version 0.3.2 (5/12/2020)
-------------------------

- fix non-local rever_kwargs

- change structure from multiple to files to one __init__ file

- update README.rst with installation instructions

version 0.3.1 (7/13/2018)
-------------------------

- found bug when calling the same decorated function multiple times.  In certain cases the 'times' keyword
argument decreased to 0 triggering a ReachedMaxRetries exception despite the function only being called once

version 0.3.0 (8/23/2017)
-------------------------

- wanted to modify behaviour to exponential backoff as default rather than fixed intervals between retrys
- to replicate functionality of previous versions include a kwarg backoff=False in your decorator

version 0.2.1 (8/8/2017)
------------------------

- realized that any function wanting to return any value would return None, so fixed that :)

version 0.2.0 (6/26/2017)
-------------------------

- specify a function to call prior to retrying
- realized that the retry count was off by 1, now it should be correct

version 0.1.0 (6/24/2017)
-------------------------

- specify whether to raise exception after all retry attempts
- included some testing
- default pause is now zero seconds

version 0.0.1 (6/23/2017)
-------------------------

- retry decorator
- specify number of times to retry
- specify number of seconds to wait
- specify which exceptions to catch