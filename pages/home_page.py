from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    URL = "https://www.guvi.in/"

    # Flexible case-insensitive locators matching <a>, <button>, or inner wrappers
    LOGIN_BUTTON = (
        By.XPATH,
        "//a[contains(translate(., 'LOGIN', 'login'), 'login') or contains(@href, 'sign-in') or @id='login-btn'] | "
        "//button[contains(translate(., 'LOGIN', 'login'), 'login') or @id='login-btn']"
    )

    SIGNUP_BUTTON = (
        By.XPATH,
        "//a[contains(translate(., 'SIGNUP', 'signup'), 'sign up') or contains(@href, 'register')] | "
        "//button[contains(translate(., 'SIGNUP', 'signup'), 'sign up')]"
    )

    COURSES_MENU = (By.XPATH, "//*[contains(translate(., 'COURSES', 'courses'), 'courses')]")
    LIVE_CLASSES_MENU = (By.XPATH, "//*[contains(translate(., 'LIVE', 'live'), 'live classes')]")
    PRACTICE_MENU = (By.XPATH, "//*[contains(translate(., 'PRACTICE', 'practice'), 'practice')]")

    # Dobby assistant container, floating widget, or chat iframe
    DOBBY_ASSISTANT = (
        By.XPATH,
        "//*[contains(@id, 'dobby') or contains(@class, 'dobby') or contains(@id, 'freshworks') or contains(@class, 'widget-container')]"
    )

    def open(self):
        self.driver.get(self.URL)
        self.wait_for_page_ready()

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def click_signup(self):
        self.click_element(self.SIGNUP_BUTTON)

    def are_menu_items_visible(self):
        return (
            self.is_displayed(self.COURSES_MENU, timeout=5) or
            self.is_displayed(self.LIVE_CLASSES_MENU, timeout=5) or
            self.is_displayed(self.PRACTICE_MENU, timeout=5)
        )

    def is_dobby_present(self):
        return (
            self.is_displayed(self.DOBBY_ASSISTANT, timeout=5) or
            len(self.driver.find_elements(By.TAG_NAME, "iframe")) > 0 or
            len(self.driver.find_elements(By.XPATH, "//div[contains(@class, 'chat')]")) > 0
        )