import os
import platform
import pytest
import allure

def pytest_configure(config):
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write("Test.Framework=Selenium+Pytest\n")
        f.write("CI.Platform=GitHub Actions\n")
        f.write("Test.Types=UI Automation\n")
        f.write("Browsers=Chrome, Firefox\n")
        f.write("Resolutions=Desktop (1920x1080), Laptop (1366x768), Tablet (1024x768), Mobile (375x667)\n")
        f.write(f"Target.URL={os.environ.get('OLLAMA_URL')}\n")
        f.write(f"Ollama.Version={os.environ.get('OLLAMA_VERSION')}\n")
        f.write(f"Ollama.Image={os.environ.get('OLLAMA_UI_IMG_TAG')}\n")
        f.write(f"YOLO.Version={os.environ.get('YOLO_VERSION')}\n")
        f.write(f"YOLO.Image={os.environ.get('YOLO_IMG_TAG')}\n")
        f.write(f"Postgres.Version={os.environ.get('POSTGRES_VERSION')}\n")

@pytest.fixture(autouse=True)
def attach_test_metadata(request):
    browser = os.environ.get("BROWSER")
    res_w = os.environ.get("SCREEN_WIDTH")
    res_h = os.environ.get("SCREEN_HEIGHT")
    resolution_pixels = f"{res_w}x{res_h}" if res_w and res_h else None
    resolution_name = os.environ.get("TEST_NAME")
    environment = os.environ.get("ENVIRONMENT")

    # Attach as Allure labels (shows in test details and for filtering)
    if browser:
        allure.dynamic.label("browser", browser)
    if resolution_name:
        allure.dynamic.label("resolution", resolution_name)
    if resolution_pixels:
        allure.dynamic.label("screen", resolution_pixels)
    if environment:
        allure.dynamic.label("environment", environment)
    for key in ["YOLO_VERSION","YOLO_IMG_TAG","OLLAMA_VERSION","OLLAMA_UI_IMG_TAG","POSTGRES_VERSION"]:
        val = os.environ.get(key)
        if val:
            allure.dynamic.label(key.lower(), val)

    # Attach as Allure attachment (shows in test attachments)
    params = [
        f"Browser: {browser}",
        f"Resolution Name: {resolution_name}",
        f"Screen: {resolution_pixels}",
        f"Environment: {environment}"
    ]
    for key in ["YOLO_VERSION","YOLO_IMG_TAG","OLLAMA_VERSION","OLLAMA_UI_IMG_TAG","POSTGRES_VERSION"]:
        val = os.environ.get(key)
        if val:
            params.append(f"{key}: {val}")
    allure.attach("\n".join(params), name="Test Metadata", attachment_type=allure.attachment_type.TEXT)
