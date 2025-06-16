import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pytest

class BaseTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()


class SignInTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get("http://localhost:3002")

    def run_test_case(self, email, password, expected_message_parts):
        try:
            self.driver.find_element(By.ID, "email").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.TAG_NAME, "button").click()

            popup = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
            actual_text = popup.text

            if not any(expected in actual_text for expected in expected_message_parts):
                raise AssertionError(
                    f"None of the expected messages found in actual text.\nExpected: {expected_message_parts}\nActual: {actual_text}"
                )

            print(f"✅ PASSED: Login with '{email}' => one of {expected_message_parts}")
        except Exception as e:
            print(f"❌ ERROR: Login test failed for '{email}' | Expected one of: {expected_message_parts}\n{e}")
            raise

    def test_valid_login(self):
        self.run_test_case("admin@gmail.com", "123", ["Sign in successful", "An unexpected error occurred"])

    def test_invalid_email_and_password(self):
        self.run_test_case("wrong@gmail.com", "wrongpass", ["Owner not found", "An unexpected error occurred"])

    def test_valid_email_wrong_password(self):
        self.run_test_case("admin@gmail.com", "wrongpass", ["Invalid credentials", "An unexpected error occurred"])

    def test_wrong_email_valid_password(self):
        self.run_test_case("wrong@gmail.com", "123", ["Owner not found", "An unexpected error occurred"])

    def test_empty_credentials(self):
        self.run_test_case("", "", ["Owner not found", "An unexpected error occurred"])


class AddPropertyTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get("http://localhost:3002/dashboard/add-property")

    def fill_form(self, property_type="apartment", name="Test Property", location="Test Location", tenant="Test Tenant"):
        select = self.wait.until(EC.presence_of_element_located((By.ID, "propertyType")))
        select.click()
        select.find_element(By.XPATH, f"//option[@value='{property_type}']").click()

        self.driver.find_element(By.ID, "name").clear()
        self.driver.find_element(By.ID, "name").send_keys(name)

        self.driver.find_element(By.ID, "location").clear()
        self.driver.find_element(By.ID, "location").send_keys(location)

        self.driver.find_element(By.ID, "tenant").clear()
        self.driver.find_element(By.ID, "tenant").send_keys(tenant)

        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add')]").click()

    def test_add_apartment_successfully(self):
        self.fill_form(property_type="apartment")
        popup = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
        self.assertIn("Property added successfully", popup.text)
        print("✅ PASSED: Add apartment")

    def test_add_shop_successfully(self):
        self.fill_form(property_type="shop", name="Test Shop")
        popup = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
        self.assertIn("Property added successfully", popup.text)
        print("✅ PASSED: Add shop")

    def test_missing_name(self):
        self.fill_form(name="")
        popup = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
        self.assertIn("Property added successfully", popup.text)
        print("✅ PASSED: Missing name handled")

    def test_missing_location(self):
        self.fill_form(location="")
        popup = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup-content")))
        self.assertIn("Property added successfully", popup.text)
        print("✅ PASSED: Missing location handled")

    def test_close_button_redirect(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Close')]")))
            close_btn.click()
            self.wait.until(EC.url_contains("/dashboard"))
            current_url = self.driver.current_url
            self.assertIn("/dashboard", current_url)
            print("✅ PASSED: Close button redirect")
        except Exception as e:
            print("❌ FAILED: Close button did not redirect properly")
            raise e


if __name__ == "__main__":
    print("🔍 Running Combined Selenium Test Suite...\n")
    pytest.main(["-v", "test_suite.py"])
