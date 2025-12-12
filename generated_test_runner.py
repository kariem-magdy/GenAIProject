import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    test_passed = True
    print("Starting Playwright tests for Login Functionality...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        base_url = "https://practicetestautomation.com/practice-test-login/"
        valid_username = "student"
        valid_password = "Password123"
        invalid_username = "incorrectUser"
        invalid_password = "incorrectPassword"

        # Locators
        username_field = page.locator("#username")
        password_field = page.locator("#password")
        submit_button = page.locator("#submit")
        error_message_div = page.locator("#error") # Error message div has id="error"

        # --- Test Scenario 1: Verify Successful Login with Valid Credentials ---
        print("\n--- Running Test Scenario 1: Verify Successful Login with Valid Credentials ---")
        try:
            await page.goto(base_url, wait_until="domcontentloaded")
            await expect(page).to_have_url(base_url)
            print("Step 1: Navigated to the login page.")

            await username_field.fill(valid_username)
            print(f"Step 2: Entered username '{valid_username}'.")
            await password_field.fill(valid_password)
            print("Step 3: Entered valid password.")
            await submit_button.click()
            print("Step 4: Clicked the 'Submit' button.")

            # Expected Result: The user is redirected to a success page, sees a success message,
            # and a logout button.
            expected_success_url = "https://practicetestautomation.com/logged-in-successfully/"
            await expect(page).to_have_url(expected_success_url)
            print(f"Step 5 (Verification): Verified new page URL contains '{expected_success_url}'.")

            # Verify new page contains expected text ('Congratulations' or 'successfully logged in')
            # Based on actual success page structure:
            await expect(page.locator("h1.post-title")).to_have_text("Logged In Successfully")
            await expect(page.locator(".post-content")).to_contain_text("Congratulations")
            print("Step 6 (Verification): Verified success messages 'Logged In Successfully' and 'Congratulations'.")

            # Verify 'Log out' link/button is displayed on the new page
            logout_link = page.get_by_role("link", name="Log out")
            await expect(logout_link).to_be_visible()
            print("Step 7 (Verification): Verified 'Log out' link is displayed.")
            print("Test Scenario 1 PASSED.")

        except Exception as e:
            print(f"Test Scenario 1 FAILED: {e}")
            test_passed = False

        # --- Test Scenario 2: Verify Unsuccessful Login with Invalid Username ---
        print("\n--- Running Test Scenario 2: Verify Unsuccessful Login with Invalid Username ---")
        try:
            await page.goto(base_url, wait_until="domcontentloaded")
            await expect(page).to_have_url(base_url)
            print("Step 1: Navigated to the login page.")

            await username_field.fill(invalid_username)
            print(f"Step 2: Entered invalid username '{invalid_username}'.")
            await password_field.fill(valid_password) # Password can be valid or invalid as per test plan
            print("Step 3: Entered a password (valid in this case).")
            await submit_button.click()
            print("Step 4: Clicked the 'Submit' button.")

            # Expected Result: An error message is displayed and the user remains on the login page.
            await expect(error_message_div).to_be_visible()
            print("Step 5 (Verification): Verified error message is displayed.")
            await expect(error_message_div).to_have_text("Your username is invalid!")
            print("Step 6 (Verification): Verified error message text is 'Your username is invalid!'.")
            await expect(page).to_have_url(base_url) # Should stay on the same page
            print("Step 7 (Verification): Verified user remained on the login page.")
            print("Test Scenario 2 PASSED.")

        except Exception as e:
            print(f"Test Scenario 2 FAILED: {e}")
            test_passed = False

        # --- Test Scenario 3: Verify Unsuccessful Login with Invalid Password ---
        print("\n--- Running Test Scenario 3: Verify Unsuccessful Login with Invalid Password ---")
        try:
            await page.goto(base_url, wait_until="domcontentloaded")
            await expect(page).to_have_url(base_url)
            print("Step 1: Navigated to the login page.")

            await username_field.fill(valid_username)
            print(f"Step 2: Entered valid username '{valid_username}'.")
            await password_field.fill(invalid_password)
            print(f"Step 3: Entered invalid password '{invalid_password}'.")
            await submit_button.click()
            print("Step 4: Clicked the 'Submit' button.")

            # Expected Result: An error message is displayed and the user remains on the login page.
            await expect(error_message_div).to_be_visible()
            print("Step 5 (Verification): Verified error message is displayed.")
            await expect(error_message_div).to_have_text("Your password is invalid!")
            print("Step 6 (Verification): Verified error message text is 'Your password is invalid!'.")
            await expect(page).to_have_url(base_url) # Should stay on the same page
            print("Step 7 (Verification): Verified user remained on the login page.")
            print("Test Scenario 3 PASSED.")

        except Exception as e:
            print(f"Test Scenario 3 FAILED: {e}")
            test_passed = False

        await browser.close()

    if test_passed:
        print("\nTEST PASSED")
    else:
        print("\nTEST FAILED")

if __name__ == "__main__":
    asyncio.run(main())