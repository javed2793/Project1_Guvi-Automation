from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        """Clicks an element, falling back to a JS click if intercepted."""
        try:
            elem = self.find_clickable(locator)
            elem.click()
        except (ElementClickInterceptedException, TimeoutException):
            elem = self.find(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            self.driver.execute_script("arguments[0].click();", elem)

    def set_text(self, locator, text):
        elem = self.find_clickable(locator)
        elem.clear()
        elem.send_keys(text)

    def is_displayed(self, locator, timeout=10):
        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return elem.is_displayed()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            return False

    def wait_for_page_ready(self, timeout=15):
        """Wait until page DOM reaches complete readyState."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title