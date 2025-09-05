import os
import platform
import pytest

@pytest.fixture(scope="session", autouse=True)
def write_allure_environment():
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
        f.write(f"URL={os.environ.get('OLLAMA_URL', 'http://localhost:3000')}\n")
        f.write(f"Environment={os.environ.get('ENVIRONMENT', 'staging')}\n")
        f.write(f"Docker Tag={os.environ.get('DOCKER_TAG', 'latest')}\n")
