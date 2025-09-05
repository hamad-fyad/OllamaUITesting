import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def write_allure_environment():
    results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    os.makedirs(results_dir, exist_ok=True)

    env_file = os.path.join(results_dir, "environment.properties")
    with open(env_file, "w") as f:
        f.write(f"URL={os.environ.get('OLLAMA_URL', 'http://localhost:3000')}\n")
        f.write(f"Browser={os.environ.get('BROWSER', 'chrome')}\n")
        f.write(f"Screen={os.environ.get('SCREEN_WIDTH', '1920')}x{os.environ.get('SCREEN_HEIGHT', '1080')}\n")
        f.write(f"Environment={os.environ.get('ENVIRONMENT', 'staging')}\n")
        f.write("Tester=Hamad Fyad\n")
