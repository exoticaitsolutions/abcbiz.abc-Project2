from datetime import datetime
from config import *
from utils import print_the_output_statement, page_load
from webdriver import pyppeteerBrowserInit
from fake_useragent import UserAgent
from pyppeteer.errors import TimeoutError as PyppeteerTimeoutError
import asyncio
import pyppeteer
from pyppeteer_stealth import stealth
from utils import print_the_output_statement


async def abiotic_login(
    username=None,
    password=None,
    output_text=None,
):
    """
    Perform login to a specified website using the provided credentials and browser settings.

    Args:
        username (str, optional): The username for the login. Defaults to None.
        password (str, optional): The password for the login. Defaults to None.
        output_text (QTextEdit, optional): A PyQt5 QTextEdit object for logging output. Defaults to None.
        loginurl (str, optional): The URL of the login page. Defaults to None.
        headless (bool, optional): Whether to run the browser in headless mode. Defaults to None.
        width (int, optional): The width of the browser window. Defaults to None.
        height (int, optional): The height of the browser window. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - status (bool): True if the login process completed, False otherwise.
            - response (str): A message indicating the result of the login process.
            - browser (Browser): The Pyppeteer browser instance.
            - page (Page): The Pyppeteer page instance.

    Raises:
        PyppeteerTimeoutError: If a timeout error occurs during the login process.
        pyppeteer.errors.NetworkError: If a network error occurs during the login process.
        Exception: If any other exception occurs during the login process.
    """
    # print_the_output_statement(output_text, "Login  Process ")
    print("Login Processing.........................")
    loop = asyncio.new_event_loop()
    print("browser init")
    # Initialize the browser
    user_agent = UserAgent().random
    print(f"Using user agent: {user_agent}")
    browser = await pyppeteerBrowserInit(HEADLESS, WIDTH, HEIGHT, user_agent)
    print("browser init completed")
    page = await browser.newPage()  # type: ignore
    # Use stealth plugin to bypass bot detection
    await stealth(page)
    await page.setViewport({"width": WIDTH, "height": HEIGHT})
    await page.setUserAgent(user_agent)
    Response = ""
    try:
        print_the_output_statement(output_text, f"Logging in to the website {LOGINURL}")
        load_page = await page_load(page, LOGINURL)
        if load_page:
            print(f"Page loaded successfully")
            await asyncio.sleep(7)
            # Perform login
            username_xpath = '//*[@id="username"]'
            await page.waitForXPath(username_xpath)
            username_element = await page.xpath(username_xpath)
            print(f"username_element  found: {username_element}")
            await username_element[0].type(username)
            print(f"Enter the username with type {username}")
            await asyncio.sleep(3)
            password_xpath = '//*[@id="password"]'
            await page.waitForXPath(password_xpath)
            password_element = await page.xpath(password_xpath)
            # await password_element[0].type('19MichaelBrewer68!')
            await password_element[0].type(password)
            print(f'Enter the password with secure password {"*" * len(password)}')
            await asyncio.sleep(3)
            login_button_xpath = '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/form/div[1]/button/span[1]'
            await page.waitForXPath(login_button_xpath)
            login_button_element = await page.xpath(login_button_xpath)
            await login_button_element[0].click()
            print("Clicked the login button...")
            await asyncio.sleep(7)
            popup_xpath = (
                '//*[@role="alertdialog"]'  # XPath for the popup message container
            )
            popup_element = await page.xpath(popup_xpath)
            print("popup_element", popup_element)
            if popup_element:
                popup_text = await (
                    await popup_element[0].getProperty("textContent")
                ).jsonValue()
                print(
                    "Popup Message:", popup_text.strip()
                )  # Print and handle the popup message text
                print_the_output_statement(output_text, popup_text.strip())
                return False, popup_text.strip(), browser, page
            else:
                # Perform further actions after login (example: clicking a button)
                target_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[1]/h1/div[2]/div/button/span/span'
                await page.waitForXPath(target_button_xpath)
                target_button_element = await page.xpath(target_button_xpath)
                await target_button_element[0].click()
                await asyncio.sleep(5)
                print("nexe button .....1")
                target_element_xpath = '//*[@id="long-menu"]/div[2]/ul/li'
                await page.waitForXPath(target_element_xpath)
                target_element = await page.xpath(target_element_xpath)
                await target_element[0].click()
                await asyncio.sleep(15)
                print("nexe button .....2")
        Response = f"Login Successfully with username={username}"
    except PyppeteerTimeoutError as timeout_error:
        print(f"timeout_error {timeout_error}")
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f"NetworkError {NetworkError}")
    except Exception as e:
        print(f"NetworkError {e}")
    print_the_output_statement(output_text, Response)
    return True, Response, browser, page


async def scrapping_data(browser=None, page=None, resource=None, output_text=None):
    """
    Scrape data from the ABC Biz website based on the provided resource details.

    Args:
        browser (object): Browser instance.
        page (object): Page instance.
        resource (list): List of records containing service numbers and last names.
        output_text (function): Function to handle output text display.

    Returns:
        tuple: A tuple containing success status (bool) and response data (str or dict).
    """
    Response = ""
    try:
        if len(resource) > 0:
            for record in resource:
                service_number = record["service_number"]
                last_name = record["last_name"]
                if service_number and last_name:
                    print(
                        f"scrapping of the data {service_number} and last name {last_name}"
                    )
                    last_name_xpath = '//*[@id="lastName"]'
                    await page.waitForXPath('//*[@id="serverId"]')
                    await page.waitForXPath(last_name_xpath)
                    server_id_element = await page.xpath('//*[@id="serverId"]')
                    print("server_id_element", server_id_element)
                    await server_id_element[0].type(service_number)
                    print(
                        f"enter the service id...........!  {service_number}",
                    )
                    last_name_element = await page.xpath(last_name_xpath)
                    print("last_name_element", last_name_element)
                    await last_name_element[0].type(last_name)
                    print(f"enter the last name ...........!  {last_name}")
                    # Click the search button
                    search_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div[2]/button[2]/span[1]'
                    await page.waitForXPath(search_button_xpath)
                    search_button_element = await page.xpath(search_button_xpath)
                    print("search_button_element", search_button_element)
                    await search_button_element[0].click()
                    print("search_button_element is clicked ")
                    await asyncio.sleep(5)
                    viewport_height = await page.evaluate("window.innerHeight")
                    print("viewport_height element is found")
                    scroll_distance = int(viewport_height * 0.2)
                    print(f"scroll_distance is  {scroll_distance}")
                    await page.evaluate(f"window.scrollBy(0, {scroll_distance})")
                    print(f"scroll_distance progress")
                    check_script = """
                                            () => {
                                                const div = document.querySelector('div.sc-gAnuJb.gzDMq');
                                                if (div) {
                                                    const pElement = div.querySelector('p');
                                                    if (pElement && pElement.textContent.trim() === 'There are no records by selected search parameters') {
                                                        return true;
                                                    }
                                                }
                                                return false;
                                            }
                                        """
                    element_exists = await page.evaluate(check_script)
                    print("element_exists", element_exists)
                    if element_exists:
                        log_entry(
                            "ERROR",
                            service_number,
                            last_name,
                            f"There are no records by selected search parameters on the service_number {service_number} and last name {last_name}",
                        )
                        print(
                            f"There are no records by selected search parameters on the service_number {service_number} and last name {last_name}",
                        )

                    else:
                        print(
                            f"data found on the {service_number}",
                        )
                        log_entry("INFO", service_number, last_name, "success")
                        print("Scrapping................................")
                        table_data = await page.evaluate(
                            """() => {
                                        const nameElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div > p > span');
                                        const serviceElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > p');
                                        const trainingElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(3) > div > div > p');
                                        const statusElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(4) > div > div > p');
                                        const expireDateElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(5) > div > div > p');

                                        return {
                                            name: nameElement ? nameElement.innerText.trim() : '',
                                            service: serviceElement ? serviceElement.innerText.trim() : '',
                                            training: trainingElement ? trainingElement.innerText.trim() : '',
                                            status: statusElement ? statusElement.innerText.trim() : '',
                                            expirationDate: expireDateElement ? expireDateElement.innerText.trim() : ''
                                        };
                                    }"""
                        )
                        if table_data:
                            table_data["reportDate"] = datetime.now().strftime(
                                "%Y-%m-%d"
                            )
                            table_data["lastName"] = (
                                last_name  # Replace with actual last name
                            )
                            Response = table_data
                    await page.waitForXPath(
                        '//button[contains(@class, "search-box-container_action-clear")]'
                    )

                    clear_button = await page.xpath(
                        '//button[contains(@class, "search-box-container_action-clear")]'
                    )
                    print("clear_button", clear_button)
                    await clear_button[0].click()
                    print("clear_button is clicked ")
                    # await page.screenshot(
                    #     {"path": f"example_{random.randint(1, 100)}.png"}
                    # )
                    print(f"Service Number: {service_number}, Last Name: {last_name}")
                else:
                    print("Please enter the vaid service number nad last name  ")
        else:
            return False, "Please enter the vaid service number nad last nam"

    except PyppeteerTimeoutError as timeout_error:
        print(f"timeout_error {timeout_error}")
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f"NetworkError {NetworkError}")
    except Exception as e:
        print(f"NetworkError {e}")
    finally:
        await browser.close()
    # print_the_output_statement(output_text, Response)
    return True, Response