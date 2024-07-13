import asyncio
from playwright.async_api import async_playwright

class ScanedUser:
    def __init__(self, name=None, time="00:00", rtlr_status='not', cookie=None):
        self.name = name
        self.time = time
        self.rtlr_status = rtlr_status
        self.cookie = cookie

    def view_data(self) -> dict:
        return {
            "name": self.name,
            "time": self.time,
            "rtlr_status": self.rtlr_status,
            "cookie": self.cookie
        }

class UserScan:
    def __init__(self, username):
        self.username = username
        self.scaned_user = ScanedUser()

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await asyncio.sleep(5)

            await page.goto("https://winair.transmaldivian.com/maintenance/timetracking/home")

            cok = await page.context.cookies()
            for cookie in cok:
                self.scaned_user.cookie = f"{cookie['name']}: {cookie['value']}"
                print(f"{cookie['name']}: {cookie['value']}")

            next_url = f'https://winair.transmaldivian.com/maintenance/timetracking/userScan.rpc?ajaxRequest=true&username={self.username}'
            print(f"Next url: {next_url}")


            if next_url:
                await page.goto(next_url)
                await page.wait_for_load_state('networkidle')

                user_info = await page.locator('span.page_title').all()
                try:
                    self.scaned_user.name = await user_info[0].inner_text()
                    self.scaned_user.time = (await user_info[1].inner_text())[-5:]
                except Exception as e:
                    print(f"Error while setting user: {e}")

                rtlt_status = await page.locator('span.system_response_alt').all()
                try:
                    self.scaned_user.rtlr_status = await rtlt_status[0].inner_text()
                except Exception as e:
                    print(f"Error while setting rtlt: {e}")

            else:
                print("No URL to navigate to in the response")

            await browser.close()
            print(self.scaned_user.view_data())
            return self.scaned_user.view_data()


async def on_scan(user):
    scan = UserScan(user)
    scan_data = await scan.run()
    return scan_data