-------
History
-------

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