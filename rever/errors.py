

class ReachedMaxRetries(Exception):
    def __init__(self, func):
        Exception.__init__(self, "Function {} raised exception due to max number of retries performed".format(func))
        self.func = func
