import pytest
import time

from rever import rever, ReachedMaxRetries


class TestRever:
    """
    Generally the types of exceptions being raised do not really matter for the tests
    # because of the default max pause time of about 1 second, more or less takes a second per test
    """

    def test_no_kwargs_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            @rever()
            def f():
                raise OSError

            f()

    def test_try_to_catch_oserror_but_miss(self):
        with pytest.raises(TypeError):
            @rever(exception=OSError)
            def f():
                raise TypeError

            f()

    def test_catch_oserror_but_ultimately_raise_no_exception(self):
        @rever(exception=OSError, raises=False)
        def f():
            raise OSError

        assert f() is None

    def test_function_args_kwargs(self):
        with pytest.raises(ReachedMaxRetries):
            @rever()
            def f(*args, **kwargs):
                if args or kwargs:
                    raise OSError

            f(1, 2, fruit="apple")

    def test_oserror_call_prior(self):
        with pytest.raises(ReachedMaxRetries):
            def g():
                return None

            @rever(prior=g)
            def f():
                raise OSError

            f()

    def test_return_value_no_errors(self):
        @rever()
        def f():
            return "does this return anything?"

        assert f() == "does this return anything?"

    def test_backoff_total_pause(self):
        @rever(total_pause=2, raises=False)
        def f():
            raise OSError

        st = time.time()
        f()
        t = time.time() - st
        assert 1 < t < 3

    def test_backoff_steps(self):
        @rever(steps=10, raises=False)
        def f():
            raise OSError

        st = time.time()
        f()
        t = time.time() - st
        assert 0 < t < 2  # cannot test steps directly but 10 steps corresponds to 1 second given default total pause

    def test_no_backoff_pause(self):
        @rever(backoff=False, pause=2, raises=False)
        def f():
            raise OSError

        st = time.time()
        f()
        t = time.time() - st
        assert 1 < t < 3

    def test_function_args_kwargs_times(self):
        with pytest.raises(ReachedMaxRetries):
            @rever(backoff=False, times=2)
            def f(*args, **kwargs):
                if args or kwargs:
                    raise OSError

            f(1, 2, fruit="apple")

    def test_multiple_uses_of_same_function_no_reached_max_tries_exception_raised(self):
        a = 1

        @rever(backoff=False, times=1, raises=True)
        def f():
            nonlocal a
            if a == 1:
                a -= 1
                raise OSError

        f()  # will catch OSError when times = 1
        f()
        f()
        # prior to v 0.3.0 calling f() repeatedly like this would trigger a ReachedMaxRetries exception
        # as the 'times' decreased to 0.  The rever_kwargs were not re-initialized with each new function call
        # and so the 'times' kept decreasing
