import os
import platform
import pytest
import allure

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
        f.write(f"Docker Tag={os.environ.get('OLLAMA_TAG', 'latest')}\n")
        f.write(f"Test Name={os.environ.get('TEST_NAME', '')}\n")

@pytest.fixture(autouse=True)
def attach_test_env(request):
    browser = os.environ.get('BROWSER', 'chrome')
    width = os.environ.get('SCREEN_WIDTH', '1920')
    height = os.environ.get('SCREEN_HEIGHT', '1080')
    tag = os.environ.get('OLLAMA_TAG', 'latest')
    env = os.environ.get('ENVIRONMENT', 'staging')
    test_name = os.environ.get('TEST_NAME', '')

    allure.dynamic.label("browser", browser)
    allure.dynamic.label("resolution", f"{width}x{height}")
    allure.dynamic.label("docker_tag", tag)
    allure.dynamic.label("environment", env)
    allure.dynamic.label("test_name", test_name)
    allure.attach(f"Browser: {browser}\nResolution: {width}x{height}\nDocker Tag: {tag}\nEnvironment: {env}\nTest Name: {test_name}",
                  name="Test Environment", attachment_type=allure.attachment_type.TEXT)
