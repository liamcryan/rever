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
    backoff = True
    total_pause = 1
    steps = 10
    times = 1
    pause = 0
    exception = BaseException
    raises = True
    prior = None

    if "backoff" not in rever_kwargs:
        rever_kwargs["backoff"] = backoff
    if "total_pause" not in rever_kwargs:
        rever_kwargs["total_pause"] = total_pause
    if "steps" not in rever_kwargs:
        rever_kwargs["steps"] = steps

    if "times" not in rever_kwargs:
        if not rever_kwargs["backoff"]:
            rever_kwargs["times"] = times
    if "pause" not in rever_kwargs:
        if not rever_kwargs["backoff"]:
            rever_kwargs["pause"] = pause

    if "exception" not in rever_kwargs:
        rever_kwargs["exception"] = exception
    if "raises" not in rever_kwargs:
        rever_kwargs["raises"] = raises
    if "prior" not in rever_kwargs:
        rever_kwargs["prior"] = prior

    initialized_kwargs = {key: rever_kwargs[key] for key in rever_kwargs}

    def rever_decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                nonlocal rever_kwargs
                if args or kwargs:
                    r = func(*args, **kwargs)
                    rever_kwargs = {key: initialized_kwargs[key] for key in initialized_kwargs}
                    return r
                else:
                    r = func()
                    rever_kwargs = {key: initialized_kwargs[key] for key in initialized_kwargs}
                    return r

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
