import os
import allure
import pytest
from dotenv import load_dotenv


def pytest_configure(config):
    # Load .env file (repo root or EC2 path)
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    os.makedirs("allure-results", exist_ok=True)
    env_file = os.path.join("allure-results", "environment.properties")

    with open(env_file, "w") as f:
        f.write("Test.Framework=Selenium+Pytest\n")
        f.write("CI.Platform=GitHub Actions\n")
        f.write("Test.Types=UI Automation\n")
        f.write("Browsers=Chrome, Firefox\n")
        f.write("Resolutions=Desktop (1920x1080), Laptop (1366x768), Tablet (1024x768), Mobile (375x667)\n")
        f.write(f"Target.URL={os.getenv('OLLAMA_URL', 'NOT_SET')}\n")
        f.write(f"Ollama.Version={os.getenv('OLLAMA_VERSION', os.getenv('IMAGE_TAG', 'NOT_SET'))}\n")
        f.write(f"Ollama.Image={os.getenv('OLLAMA_UI_IMAGE', os.getenv('OLLAMA_UI_IMG_TAG', 'NOT_SET'))}\n")
        f.write(f"YOLO.Version={os.getenv('YOLO_VERSION', 'NOT_SET')}\n")
        f.write(f"YOLO.Image={os.getenv('YOLO_IMAGE', os.getenv('YOLO_IMG_TAG', 'NOT_SET'))}\n")
        f.write(f"Postgres.Version={os.getenv('POSTGRES_VERSION', 'NOT_SET')}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    browser = os.environ.get("BROWSER")
    res_w = os.environ.get("SCREEN_WIDTH")
    res_h = os.environ.get("SCREEN_HEIGHT")
    resolution_pixels = f"{res_w}x{res_h}" if res_w and res_h else None
    resolution_name = os.environ.get("TEST_NAME")  # or matrix.resolution.name passed in env
    environment = os.environ.get("ENVIRONMENT")

    # Expose as Allure parameters
    if browser:
        allure.dynamic.parameter("browser", browser)
    if resolution_name:
        allure.dynamic.parameter("resolution", resolution_name)
    if resolution_pixels:
        allure.dynamic.parameter("screen", resolution_pixels)
    if environment:
        allure.dynamic.parameter("environment", environment)

    # Keep labels for filtering/search
    with allure.step("Test metadata"):
        if browser:
            allure.dynamic.label("browser", browser)
        if resolution_name:
            allure.dynamic.label("resolution", resolution_name)
        if resolution_pixels:
            allure.dynamic.label("screen", resolution_pixels)
        if environment:
            allure.dynamic.label("environment", environment)

        # Attach service versions from env
        for key in [
            "YOLO_VERSION",
            "YOLO_IMAGE",
            "YOLO_IMG_TAG",
            "OLLAMA_VERSION",
            "OLLAMA_UI_IMAGE",
            "OLLAMA_UI_IMG_TAG",
            "POSTGRES_VERSION",
            "IMAGE_TAG",
        ]:
            val = os.getenv(key)
            if val:
                allure.dynamic.label(key.lower(), val)

    yield
