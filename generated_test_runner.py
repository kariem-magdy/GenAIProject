import asyncio
from playwright.async_api import async_playwright, expect

# Constants
BASE_URL = "https://practicetestautomation.com/practice-test-login/"
SUCCESS_PAGE_FULL_URL = "https://practicetestautomation.com/logged-in-successfully/"
VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass" # Using an invalid password as well, but the page's validation prioritizes username.
ERROR_MESSAGE_TEXT_USERNAME_INVALID = "Your username is invalid!"
MOBILE_VIEWPORT = {"width": 375, "height": 667}

async def main():
    all_tests_passed = True # Flag to track overall test status

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print(f"Starting tests for: {BASE_URL}\n")

        # --- Test Scenario 1: Verify Successful Login with Valid Credentials ---
        scenario_name_1 = "Scenario 1: Successful Login"
        print(f"--- Running {scenario_name_1} ---")
        try:
            await page.goto(BASE_URL)
            await page.locator("#username").fill(VALID_USERNAME)
            await page.locator("#password").fill(VALID_PASSWORD)
            await page.locator("#submit").click()

            # Assertions for successful login
            await expect(page).to_have_url(SUCCESS_PAGE_FULL_URL)
            await expect(page.locator(".post-title")).to_have_text("Logged In Successfully")
            await expect(page.locator(".wp-block-button__link", has_text="Log out")).to_be_visible()

            print(f"{scenario_name_1}: PASSED\n")
        except Exception as e:
            print(f"{scenario_name_1}: FAILED - {e}\n")
            all_tests_passed = False
            await page.screenshot(path=f"failed_{scenario_name_1.replace(' ', '_').lower()}.png")
        finally:
            # Navigate back to the login page for the next test scenario
            await page.goto(BASE_URL)

        # --- Test Scenario 2: Verify Login Failure with Invalid Credentials and Error Message ---
        scenario_name_2 = "Scenario 2: Invalid Login (Wrong Username)"
        print(f"--- Running {scenario_name_2} ---")
        try:
            # Ensure we are on the login page
            await page.goto(BASE_URL) # Ensure fresh state
            await page.locator("#username").fill(INVALID_USERNAME)
            await page.locator("#password").fill(INVALID_PASSWORD)
            await page.locator("#submit").click()

            # Assertions for invalid login
            error_message_locator = page.locator("#error")
            await expect(error_message_locator).to_be_visible()
            await expect(error_message_locator).to_have_text(ERROR_MESSAGE_TEXT_USERNAME_INVALID)
            await expect(page).to_have_url(BASE_URL) # Should remain on the login page URL

            print(f"{scenario_name_2}: PASSED\n")
        except Exception as e:
            print(f"{scenario_name_2}: FAILED - {e}\n")
            all_tests_passed = False
            await page.screenshot(path=f"failed_{scenario_name_2.replace(' ', '_').lower()}.png")
        finally:
            # Clear fields and reload for a clean state before next test
            await page.locator("#username").fill("")
            await page.locator("#password").fill("")
            await page.reload() # Ensures clean state after potential error display

        # --- Test Scenario 3: Verify Mobile Navigation Toggle Functionality ---
        scenario_name_3 = "Scenario 3: Mobile Navigation Toggle"
        print(f"--- Running {scenario_name_3} ---")
        try:
            # Set mobile viewport
            await page.set_viewport_size(MOBILE_VIEWPORT)
            await page.goto(BASE_URL) # Reload the page with the new viewport

            toggle_button_locator = page.locator("#toggle-navigation")
            # Locate an element inside the mobile menu to verify its visibility
            home_menu_item_locator = page.locator("#mobile-menu-container >> text=Home")

            # Assert menu is initially hidden
            await expect(home_menu_item_locator).not_to_be_visible()

            # Click to show menu
            await toggle_button_locator.click()
            await expect(home_menu_item_locator).to_be_visible()

            # Click to hide menu
            await toggle_button_locator.click()
            await expect(home_menu_item_locator).not_to_be_visible()

            print(f"{scenario_name_3}: PASSED\n")
        except Exception as e:
            print(f"{scenario_name_3}: FAILED - {e}\n")
            all_tests_passed = False
            await page.screenshot(path=f"failed_{scenario_name_3.replace(' ', '_').lower()}.png")
        finally:
            # Reset viewport to default desktop size for proper browser closure or subsequent tests
            await page.set_viewport_size({"width": 1280, "height": 720})

        await browser.close()

    # --- Final Test Result Output ---
    if all_tests_passed:
        print("\nTEST PASSED")
    else:
        print("\nTEST FAILED")

if __name__ == "__main__":
    asyncio.run(main())