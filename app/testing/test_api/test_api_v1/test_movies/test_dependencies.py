from api.api_v1.movies.dependencies import UNSAFE_METHODS

SAFE_METHODS = {
    "GET",
    "HEAD",
    "OPTIONS",
}


def test_unsafe_methods_doesnt_contain_safe_methods() -> None:
    assert not UNSAFE_METHODS & SAFE_METHODS
