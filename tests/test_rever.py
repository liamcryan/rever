import pytest

from rever import rever
from rever.errors import ReachedMaxRetries


class TestRever:
    """
    Generally the types of exceptions being raised do not really matter for the tests
    """
    def test_no_kwargs_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            @rever()
            def f():
                raise OSError
            f()

    def test_oserror_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            @rever(exception=OSError)
            def f():
                raise OSError
            f()

    def test_typerror_raise_typeerror(self):
        with pytest.raises(TypeError):
            @rever(exception=OSError)
            def f():
                raise TypeError
            f()

    def test_oserror_raise_no_exception(self):
        @rever(exception=OSError, raises=False)
        def f():
            raise OSError
        assert f() is None

    def test_function_args_kwargs_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            @rever()
            def f(*args, **kwargs):
                if args or kwargs:
                    raise OSError
            f(1, 2, fruit="apple")

    def test_function_args_kwargs_two_retrys_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            @rever(times=2)
            def f(*args, **kwargs):
                if args or kwargs:
                    raise OSError

            f(1, 2, fruit="apple")

    def test_oserror_call_prior_raise_max_retries(self):
        with pytest.raises(ReachedMaxRetries):
            def g():
                return None

            @rever(prior=g)
            def f():
                raise OSError
            f()
