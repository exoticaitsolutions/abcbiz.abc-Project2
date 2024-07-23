import asyncio
from pyppeteer import launch
from config import HEADLESS, HEIGHT, WIDTH
from utils import find_chrome_path


def pyppeteerBrowserInit(loop):
    """
    Initializes a Pyppeteer browser instance with specified settings.
    Args:
        loop (asyncio.AbstractEventLoop): The asyncio event loop to be used for launching the browser.

    Returns:
        pyppeteer.browser.Browser or (None, None): Returns the initialized browser instance if successful;
                                                   otherwise, returns (None, None) if an error occurs.

    Raises:
        Exception: If there is an error while initializing the browser.
    """
    executable_path = find_chrome_path()
    print("executable_path", executable_path)
    print(f"window size: {WIDTH}x{HEIGHT}")
    # print(f"Using user agent: {USERAGENT}")
    asyncio.set_event_loop(loop)
    try:
        browser = loop.run_until_complete(
            launch(
                executablePath=executable_path,
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    # f"--user-agent={USERAGENT}"
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    f"--window-size={WIDTH},{HEIGHT}",
                    "--start-maximized",
                    "--disable-notifications",
                    "--disable-popup-blocking",
                    "--ignore-certificate-errors",
                    "--allow-file-access",
                ],
            )
        )
        return browser
    except Exception as e:
        # Print the error and return None if an exception occurs
        print(f"Error initializing browser: {e}")
        return None, None
