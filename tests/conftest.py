import os
import platform
import pytest
import sys

@pytest.fixture(scope="session", autouse=True)
def write_allure_environment():
    """
    Automatically create allure-results/environment.properties
    with general system info.
    """
    results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    os.makedirs(results_dir, exist_ok=True)

    env_file = os.path.join(results_dir, "environment.properties")
    with open(env_file, "w") as f:
        f.write(f"OS={platform.system()} {platform.release()}\n")
        f.write(f"OS Version={platform.version()}\n")
        f.write(f"Python={platform.python_version()}\n")
        f.write(f"Processor={platform.processor()}\n")
        f.write(f"Architecture={platform.architecture()[0]}\n")
        f.write(f"Tester=Hamad Fyad\n")