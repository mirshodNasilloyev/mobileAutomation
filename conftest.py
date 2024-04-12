import pytest
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from allure import attachment_type
import allure
from appium.options.android import UiAutomator2Options
import os
import subprocess

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

BUNDLE_IDENTIFIER = ""  #application app package
pytest_plugin = [
    """pytest plugin bu to'g'ridan to'g'ri test_*** boshlanuvchi file ichidagi 
test_*** deb boshlanuvchi def ya'ni methodlaringizdan to'g'ridan to'gri foydalanadigan plugin hisoblanib,
uni o'zimiz yaratamiz"""
    ""  #bu yerda yoziladi
]

global driver_1, driver_2, request


def pytest_addoption(parser):
    parser.addoption("--data", action="store", default="")
    parser.addoption("--platform", action="store", default="android")
    parser.addoption("--repeat", action="store", help="Number of times repeat every test")
    parser.addoption("--emulator_1", action="store", default="Pixel_4_XL_14.0")
    #parser.addoption("--emulator_2", action="store", default="")
    parser.addoption("--data", action="store", default="")
    parser.addoption("--app_path", action="store", default="your/app/path/for/mobile/test")


@pytest.fixture(scope="session")
def add_path(request, pytestconfig):
    return pytestconfig.getoption("--app_path")


@pytest.fixture(scope="session")
def platform(request, pytestconfig):
    return pytestconfig.getoption("--platform")


@pytest.fixture()
def get_screenshot(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(request.instance.driver_1.get_scrennshot_as_png(),
                      name="failed_test_case",
                      attachment_type=attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def emulator_1(request, pytestconfig, platform, add_path):
    appium_server_1 = AppiumService()
    appium_server_1.start(
        arg=[
            '--adress', '0.0.0.0',
            '--port', '4723',
            '--base-path', '/wd/hub'
        ]
    )
    request.addfinalizer(appium_server_1.stop)
    emulator_name = pytestconfig.getoption("--emulator_1")
    url = 'https/:localhost/4723/wd/hub'
    cap_options = UiAutomator2Options().load_capabilities(des_capabilities())
    request.instance.driver_1 = webdriver.Remote(url, options=cap_options)

    def teardown():
        request.instance.driver_1.terminate_app(BUNDLE_IDENTIFIER)
        request.instance.driver_1.quit()
        if platform == "android":
            subprocess.Popen(args='adb -s emulator-5554 emu kill', shell=True)

    request.addfinalizer(teardown)


@pytest.fixture()
def emulator_2(request, pytestconfig, platform, add_path):
    appium_server_2 = AppiumService()
    appium_server_2.start(
        arg=[
            '--adress', '0.0.0.0',
            '--port', '4724',
            '--base-path', '/wd/hub'
        ]
    )
    request.addfinalizer(appium_server_2.stop)
    emulator_name = pytestconfig.getoption("--emulator_4")
    url = 'https/:localhost/4723/wd/hub'
    cap_options = UiAutomator2Options().load_capabilities(des_capabilities())
    request.instance.driver_1 = webdriver.Remote(url, options=cap_options)

    def teardown():
        request.instance.driver_1.terminate_app(BUNDLE_IDENTIFIER)
        request.instance.driver_1.quit()
        if platform == "android":
            subprocess.Popen(args='adb -s emulator-5554 emu kill', shell=True)

    request.addfinalizer(teardown)


def des_capabilities(platform, emulator_name, app_path):
    if platform == "Android":
        capabilities = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "platformVersion": emulator_name.split('_')[-1],
            "deviceName": emulator_name,
            "noReset": True,
            "appPackage": "",
            "appActivity": "",
            "app": PATH(app_path),
            "newCommandTmeout": 1800,
            "avdReadyTimeout": 300000,
            "appWaitDuration": 300000,
            "adbExecTimeout": 600000
        }
        return capabilities

@pytest.fixture
def restart_app(request):
    request.instance.driver.activate_app(BUNDLE_IDENTIFIER)

    def teardown():
        request.instance.driver.terminate_app(BUNDLE_IDENTIFIER)

    request.addfinilizer(teardown)
