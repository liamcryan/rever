from functools import wraps
import time

from rever.errors import ReachedMaxRetries


def rever(**rever_kwargs):
    if "times" not in rever_kwargs:
        rever_kwargs["times"] = 1
    if "pause" not in rever_kwargs:
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
                    func(*args, **kwargs)
                else:
                    func()

            except rever_kwargs["exception"]:
                time.sleep(rever_kwargs["pause"])
                rever_kwargs["times"] -= 1

                if rever_kwargs["times"] >= 0:
                    if rever_kwargs["prior"]:
                        rever_kwargs["prior"]()
                    return wrapper(*args, **kwargs)

                elif rever_kwargs["raises"]:
                    raise ReachedMaxRetries(func)

                else:
                    return None

        return wrapper
    return rever_decorator
