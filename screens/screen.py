import time

from appium.common.exceptions import NoSuchContextException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.appiumby import AppiumBy


class Screen:

    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator):
        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_element_by_method(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    self.get_element_by_method(method, value)
                except NoSuchContextException as e:
                    print("Error during getting locator", e.msg, "and element: ", values)
            raise Exception("No Such a element located:", values)

    def get_element_by_method(self, method, value):
        if method == "accessibility_id":
            return WebDriverWait(self.driver, 30).until(
                ec.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, value)))
        elif method == "xpath":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((AppiumBy.XPATH, value)))
        elif method == "id":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((AppiumBy.ID, value)))
        elif method == "class":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((AppiumBy.CLASS_NAME, value)))
        elif method == "name":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((AppiumBy.NAME, value)))

    def get_elements(self, locator):
        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_elements_by_method(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    self.get_elements_by_method(method, value)
                except NoSuchContextException as e:
                    print("Error during getting locator", e.msg, "and element: ", values)
            raise Exception("No Such a element located:", values)

    def get_elements_by_method(self, method, value):
        if method == "accessibility_id":
            return WebDriverWait(self.driver, 30).until(
                ec.visibility_of_all_elements_located((AppiumBy.ACCESSIBILITY_ID, value)))
        elif method == "xpath":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_all_elements_located((AppiumBy.XPATH, value)))
        elif method == "id":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_all_elements_located((AppiumBy.ID, value)))
        elif method == "class":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_all_elements_located((AppiumBy.CLASS_NAME, value)))
        elif method == "name":
            return WebDriverWait(self.driver, 30).until(ec.visibility_of_all_elements_located((AppiumBy.NAME, value)))

    def is_element_exist(self, locator):
        try:
            return self.get_element(locator).is_displayed()
        except NoSuchContextException as e:
            print("Error during getting locator:", e.msg, "and element: ", locator[1])
        return False

    def click(self, locator):
        self.get_element(locator).click()

    def clear_text_of_input_field(self, locator):
        self.get_element(locator).clear()

    def get_element_text(self, locator):
       return self.get_element(locator).text

    def enter_data(self, locator):
        self.get_element(locator).send_keys()

    def click_by_keyCode(self, key_code):
        self.driver.press_keycode(key_code)

    def hide_keyboard(self):
        try:
            time.sleep(1)
            self.driver.hide_keyboard()
        except Exception:


