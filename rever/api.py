from functools import wraps
import time

from rever.errors import ReachedMaxRetries


def rever(**rever_kwargs):
    """

    rever_kwargs default values defined:

    If backoff is True, then times and pause will not be initialized, but they will be calculated.
    backoff: True
    total_pause: 30
    steps: 10
    exception: BaseException
    raises: True
    prior: None

    If backoff is False, then total_pause and steps will be initialized, but do not get used.
    backoff: False
    times: 1
    pause: 0
    exception: BaseException
    raises: True
    prior: None
    """

    if "backoff" not in rever_kwargs:
        rever_kwargs["backoff"] = True
    if "total_pause" not in rever_kwargs:
        rever_kwargs["total_pause"] = 1
    if "steps" not in rever_kwargs:
        rever_kwargs["steps"] = 10

    if "times" not in rever_kwargs:
        if not rever_kwargs["backoff"]:
            rever_kwargs["times"] = 1
    if "pause" not in rever_kwargs:
        if not rever_kwargs["backoff"]:
            rever_kwargs["pause"] = 0

    if "exception" not in rever_kwargs:
        rever_kwargs["exception"] = BaseException
    if "raises" not in rever_kwargs:
        rever_kwargs["raises"] = True
    if "prior" not in rever_kwargs:
        rever_kwargs["prior"] = None

    def rever_decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if args or kwargs:
                    return func(*args, **kwargs)
                else:
                    return func()

            except rever_kwargs["exception"]:

                if rever_kwargs["backoff"]:
                    rever_kwargs["pause"] = \
                        .5 * (rever_kwargs["total_pause"] / 2 ** (rever_kwargs["steps"]))

                    if rever_kwargs["steps"] >= 0:
                        time.sleep(rever_kwargs["pause"])
                        rever_kwargs["steps"] -= 1

                        if rever_kwargs["prior"]:
                            rever_kwargs["prior"]()

                        return wrapper(*args, **kwargs)
                else:
                    if rever_kwargs["times"] > 0:
                        time.sleep(rever_kwargs["pause"])
                        rever_kwargs["times"] -= 1

                        if rever_kwargs["prior"]:
                            rever_kwargs["prior"]()

                        return wrapper(*args, **kwargs)

                if rever_kwargs["raises"] and (rever_kwargs["steps"] < 0 or rever_kwargs["times"] <= 0):
                    raise ReachedMaxRetries(func)
                else:
                    return None

        return wrapper
    return rever_decorator
