import pytest

from rever import ReachedMaxRetries
from rever import rever


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
