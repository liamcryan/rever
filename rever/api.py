from functools import wraps
import time


def rever(**rever_kwargs):
    if "times" not in rever_kwargs:
        rever_kwargs["times"] = 1
    if "pause" not in rever_kwargs:
        rever_kwargs["pause"] = 1
    if "exception" not in rever_kwargs:
        rever_kwargs["exception"] = BaseException

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
                print("rever is about to retry this function: {}".format(func),
                      "\n",
                      "After this attempt, there will be {} more attempts".format(rever_kwargs["times"]))
                if rever_kwargs["times"] > 0:
                    return wrapper(*args, **kwargs)

        return wrapper
    return rever_decorator