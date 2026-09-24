import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.home_page import HomePage
from pages.login_page import LoginPage


# TC-1: Verify whether URL is valid
def test_tc1_verify_url(driver):
    home = HomePage(driver)
    home.open()
    assert "guvi.in" in home.get_current_url()


# TC-2: Verify whether the title of the webpage is correct
def test_tc2_verify_title(driver):
    home = HomePage(driver)
    home.open()
    assert "GUVI" in home.get_title()


# TC-3: Verify visibility and clickability of Login button
def test_tc3_login_button(driver):
    home = HomePage(driver)
    home.open()
    assert home.is_displayed(home.LOGIN_BUTTON), "Login button is not visible"
    home.click_login()
    WebDriverWait(driver, 10).until(lambda d: "sign-in" in d.current_url or "login" in d.current_url)
    assert any(x in driver.current_url for x in ["sign-in", "login"])


# TC-4: Verify visibility and clickability of Sign-Up button
def test_tc4_signup_button(driver):
    home = HomePage(driver)
    home.open()
    assert home.is_displayed(home.SIGNUP_BUTTON), "Sign-up button is not visible"
    home.click_signup()
    WebDriverWait(driver, 10).until(lambda d: "register" in d.current_url or "sign-up" in d.current_url)
    assert any(x in driver.current_url for x in ["register", "sign-up"])


# TC-5: Verify navigation to the Sign-In/Register page via Sign-Up button
def test_tc5_register_navigation(driver):
    home = HomePage(driver)
    home.open()
    home.click_signup()
    WebDriverWait(driver, 10).until(lambda d: "register" in d.current_url or "sign-up" in d.current_url)
    assert "guvi.in" in driver.current_url and any(x in driver.current_url for x in ["register", "sign-up"])


# TC-6: Verify login functionality with valid credentials
def test_tc6_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("validusername@gmail.com", "valid password")
    WebDriverWait(driver, 15).until(lambda d: "sign-in" not in d.current_url)
    assert "guvi.in" in driver.current_url and "sign-in" not in driver.current_url


# TC-7: Verify login with invalid credentials
def test_tc7_invalid_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_dummy_account@testdomain.com", "WrongPassword123")
    assert login_page.is_error_displayed()


# TC-8: Verify that menu items like "Courses", "LIVE Classes", and "Practice" are displayed
def test_tc8_menu_items(driver):
    home = HomePage(driver)
    home.open()
    assert home.are_menu_items_visible()


# TC-9: Validate that the Dobby Guvi Assistant is present on the page
def test_tc9_dobby_assistant(driver):
    home = HomePage(driver)
    home.open()
    assert home.is_dobby_present()


# TC-10: Validate logout functionality
def test_tc10_logout_functionality(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("javed2793@gmail.com", "Izhaan@2793")
    login_page.logout()

    # Verify redirected back to login or homepage as specified in test requirements
    current_url = driver.current_url.rstrip("/")
    assert ("sign-in" in current_url) or (current_url in ["https://www.guvi.in", "https://guvi.in"])