import pytest

from rever import rever
from rever.errors import ReachedMaxRetries


class TestRever:
    """
    Generlly the types of exceptions being raised do not really matter for the tests
    """
    def test_rever_no_kwargs(self):
        with pytest.raises(ReachedMaxRetries):
            @rever()
            def f():
                raise OSError
            f()

    def test_rever_oserror(self):
        with pytest.raises(ReachedMaxRetries):
            @rever(exception=OSError)
            def f():
                raise OSError
            f()

    def test_rever_typerror_not_retried(self):
        with pytest.raises(TypeError):
            @rever(exception=OSError)
            def f():
                raise TypeError
            f()

    def test_rever_oserror_raise_no_exception(self):
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

    def test_function_args_kwargs_two_retys(self):
        with pytest.raises(ReachedMaxRetries):
            @rever(times=2)
            def f(*args, **kwargs):
                if args or kwargs:
                    raise OSError

            f(1, 2, fruit="apple")

