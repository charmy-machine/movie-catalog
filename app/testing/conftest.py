from os import getenv

import pytest

if getenv("TESTING") != "1":
    error_msg = "Environment is not ready for testing."
    pytest.exit(error_msg)
