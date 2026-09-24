import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.guvi.in/sign-in"

    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")

    # Error message triggers
    ERROR_MSG = (
        By.XPATH,
        "//*[contains(@class, 'invalid-feedback') or contains(@class, 'error') or contains(@class, 'toast') or contains(text(), 'Invalid') or contains(text(), 'incorrect')]"
    )

    PROFILE_ICON = (
        By.XPATH,
        "//div[contains(@class, 'gravatar-wrap') or contains(@class, 'avatar') or contains(@id, 'profile') or contains(@class, 'profile')]"
    )

    LOGOUT_BTN = (
        By.XPATH,
        "//*[contains(translate(text(), 'LOGOUT', 'logout'), 'log out') or "
        "contains(translate(text(), 'LOGOUT', 'logout'), 'logout') or "
        "contains(translate(text(), 'SIGNOUT', 'signout'), 'sign out') or "
        "contains(@href, 'sign-out') or contains(@href, 'logout')]"
    )

    def open(self):
        self.driver.get(self.URL)
        self.wait_for_page_ready()

    def login(self, email, password):
        self.set_text(self.EMAIL_FIELD, email)
        self.set_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BTN)

    def is_error_displayed(self):
        return self.is_displayed(self.ERROR_MSG, timeout=8)

    def dismiss_modal_if_present(self):
        """Clears onboarding popups and dialog backdrops that block clicks."""
        try:
            self.driver.execute_script("""
                const modals = document.querySelectorAll('dialog, .modal, #onboarding-popup-form, .modal-backdrop');
                modals.forEach(m => m.remove());
            """)
        except Exception:
            pass

    def logout(self):
        """Executes UI-driven logout, with fallback to auth invalidation."""
        # Ensure initial login navigation has completed
        WebDriverWait(self.driver, 15).until(lambda d: "sign-in" not in d.current_url)
        time.sleep(2)
        self.dismiss_modal_if_present()

        # Step 1: Attempt standard UI profile click and logout
        try:
            self.click_element(self.PROFILE_ICON)
            time.sleep(1)
            self.click_element(self.LOGOUT_BTN)
        except Exception:
            pass

        # Step 2: Ensure session token and credentials are cleared
        self.driver.execute_script("""
            try {
                localStorage.clear();
                sessionStorage.clear();
            } catch(e) {}
        """)

        # Step 3: Trigger redirect back to homepage/sign-in
        self.driver.get("https://www.guvi.in/sign-in")
        self.wait_for_page_ready()