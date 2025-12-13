import asyncio
from playwright.async_api import async_playwright

async def test_successful_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://practicetestautomation.com/practice-test-login/")

        # Locate and fill username and password
        await page.locator("#username").fill("student")
        await page.locator("#password").fill("Password123")

        # Click submit button
        await page.locator("#submit").click()

        # Verify successful login
        try:
            await page.wait_for_url("https://practicetestautomation.com/logged-in-successfully/")
            assert "Congratulations" in await page.content()
            assert await page.locator("button:has-text('Log out')").is_visible()
            print("Test Scenario 1: Successful Login with Valid Credentials - TEST PASSED")
        except Exception as e:
            print(f"Test Scenario 1: Successful Login with Valid Credentials - TEST FAILED: {e}")
        finally:
            await browser.close()

async def test_failed_login_invalid_credentials():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://practicetestautomation.com/practice-test-login/")

        # Locate and fill invalid username and password
        await page.locator("#username").fill("invaliduser")
        await page.locator("#password").fill("wrongpassword")

        # Click submit button
        await page.locator("#submit").click()

        # Verify failed login and error message
        try:
            assert await page.locator("#error").is_visible()
            assert await page.locator("#error").text_content() == "Your username is invalid!"
            print("Test Scenario 2: Failed Login with Invalid Credentials - TEST PASSED")
        except Exception as e:
            print(f"Test Scenario 2: Failed Login with Invalid Credentials - TEST FAILED: {e}")
        finally:
            await browser.close()

async def test_navigation_link_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://practicetestautomation.com/practice-test-login/")

        # Locate and click the Home link
        home_link = page.locator("//a[text()='Home']")
        assert await home_link.is_visible()
        await home_link.click()

        # Verify navigation
        try:
            await page.wait_for_url("https://practicetestautomation.com/")
            print("Test Scenario 3: Navigation Link Verification - TEST PASSED")
        except Exception as e:
            print(f"Test Scenario 3: Navigation Link Verification - TEST FAILED: {e}")
        finally:
            await browser.close()

async def main():
    await test_successful_login()
    await test_failed_login_invalid_credentials()
    await test_navigation_link_verification()

if __name__ == "__main__":
    asyncio.run(main())