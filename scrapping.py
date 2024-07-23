from datetime import datetime
from config import *
from utils import parse_json, print_the_output_statement, page_load
from pyppeteer.errors import TimeoutError as PyppeteerTimeoutError
import asyncio
import pyppeteer
import math
from pyppeteer_stealth import stealth


async def abiotic_login(browser, username, password, output_text):
    page = await browser.newPage()  # type: ignore
    await stealth(page)
    await page.setViewport({"width": WIDTH, "height": HEIGHT})
    Response = ""
    try:
        print_the_output_statement(output_text, f"Logging in to the website {LOGINURL}")
        load_page = await page_load(page, LOGINURL)
        if load_page:
            await asyncio.sleep(10)
            # Select the element using XPath
            element_404_error = await page.xpath(
                '//span[@style="margin-left: 450px; margin-top: 120px; font-size: 120px; color: rgb(122, 124, 125); font-weight: 900; display: inline; position: absolute;"]'
            )
            if element_404_error:
                text = "Internal Error Occurred while running application. Please Try Again!!"
                print(f"error {text}")
                return False, text, "", ""
            else:
                # Username Elements
                username_selector = (
                    "#username"  # CSS selector for the element with id 'username'
                )
                await page.waitForSelector(username_selector)
                username_element = await page.querySelector(username_selector)
                await username_element.type(username)
                print(f"Enter the username with type {username}")
                await asyncio.sleep(3)
                # Password
                password_selector = (
                    "#password"  # CSS selector for the element with id 'password'
                )
                await page.waitForSelector(password_selector)
                password_element = await page.querySelector(password_selector)
                await password_element.type(password)
                print(f'Enter the password with secure password {"*" * len(password)}')
                await asyncio.sleep(3)
                # Login Button Clicked
                login_button_selector = "button.abc-login_submit-button_Sl8_I"  # CSS selector for the button with the specific class
                await page.waitForSelector(login_button_selector)
                login_button = await page.querySelector(login_button_selector)
                await login_button.click()
                print("Login button clicked")
                await asyncio.sleep(7)
                popup_selector = '[role="alertdialog"]'  # CSS selector for the element with role="alertdialog"
                popup_element = await page.querySelector(popup_selector)
                if popup_element:
                    popup_text = await popup_element.querySelectorEval(
                        "pre", "node => node.innerText"
                    )
                    print("popup_text", popup_text)
                    return False, popup_text, "", ""
                else:
                    # Select the button by its aria-label and click it
                    button_aria_label = "Switch Dashboard"
                    button_selector = f'[aria-label="{button_aria_label}"]'
                    await page.waitForSelector(button_selector)
                    button_element = await page.querySelector(button_selector)
                    await button_element.click()
                    print(f'Clicked the button with aria-label "{button_aria_label}"')
                    await asyncio.sleep(5)
                    # Second
                    target_element_xpath = '//*[@id="long-menu"]/div[2]/ul/li'
                    await page.waitForXPath(target_element_xpath)
                    target_element = await page.xpath(target_element_xpath)
                    await target_element[0].click()
                    await asyncio.sleep(10)
                    print("nexe button .....2")
                    Response = f"Login Successfully with username={username}"
                    return True, Response, browser, page
        else:
            text = (
                "Internal Error Occurred while running application. Please Try Again!!"
            )
            return False, text, "", ""
    except PyppeteerTimeoutError as timeout_error:
        print(f"timeout_error {timeout_error}")
        return (
            False,
            "Internal Error Occurred while running application. Please Try Again!!",
            "",
            "",
        )
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f"NetworkError {NetworkError}")
        return (
            False,
            "Internal Error Occurred while running application. Please Try Again!!",
            "",
            "",
        )
    except Exception as e:
        # Handle exceptions gracefully
        print(f"Exception occurred during login: {e}")
        print_the_output_statement(output_text, f"Login Process Failed: {str(e)}")
        return False, f"Login Process Failed: {str(e)}", "", ""


async def scrapping_data(browser, page, json_data, output_text):
    print("scrapping_data")
    json_object = parse_json(json_data)
    total_records = len(json_object)
    print_the_output_statement(output_text, f"Total Number of Records {total_records}")
    Response = []
    try:
        for index, record in enumerate(json_object):
            print_the_output_statement(
                output_text, f"Processing record {index + 1} out of {total_records}"
            )
            table_data = {}  # Initialize table_data for each record
            service_number = (
                ""
                if math.isnan(record.get("Server_ID", float("nan")))
                else int(record["Server_ID"])
            )
            last_name = record.get("Last_Name", "")

            if service_number and last_name:
                last_name_xpath = '//*[@id="lastName"]'
                await page.waitForXPath('//*[@id="serverId"]')
                await page.waitForXPath(last_name_xpath)

                server_id_element = await page.xpath('//*[@id="serverId"]')
                await server_id_element[0].type(str(service_number))

                last_name_element = await page.xpath(last_name_xpath)
                await last_name_element[0].type(last_name)

                # Click the search button
                search_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div[2]/button[2]/span[1]'
                await page.waitForXPath(search_button_xpath)
                search_button_element = await page.xpath(search_button_xpath)
                await search_button_element[0].click()

                await asyncio.sleep(5)

                viewport_height = await page.evaluate("window.innerHeight")
                scroll_distance = int(viewport_height * 0.2)
                await page.evaluate(f"window.scrollBy(0, {scroll_distance})")

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

                if element_exists:
                    table_data.update(
                        {
                            "expirationDate": "",
                            "lastName": last_name,
                            "reportDate": datetime.now().strftime("%Y-%m-%d"),
                            "service": service_number,
                            "status": "",
                            "training": "",
                            "record status": "No data found",
                        }
                    )
                    Response.append(table_data)
                    # log_entry("ERROR", service_number, last_name, "No data found")
                    print_the_output_statement(
                        output_text,
                        (
                            f"No Data found for service number {service_number} and last name {last_name}"
                        ),
                    )
                    # print(
                    #     f"There are no records by selected search parameters for service number {service_number} and last name {last_name}")

                else:
                    print(f"Data found for service number {service_number}")
                    print_the_output_statement(
                        output_text,
                        (
                            f"Data found for service number {service_number} and last name {last_name}"
                        ),
                    )
                    # log_entry("INFO", service_number, last_name, "success")

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
                        table_data.update(
                            {
                                "reportDate": datetime.now().strftime("%Y-%m-%d"),
                                "lastName": last_name,
                                "record status": "success",
                            }
                        )
                        Response.append(table_data)

                await page.waitForXPath(
                    '//button[contains(@class, "search-box-container_action-clear")]'
                )
                clear_button = await page.xpath(
                    '//button[contains(@class, "search-box-container_action-clear")]'
                )
                await clear_button[0].click()
            else:
                table_data.update(
                    {
                        "expirationDate": "",
                        "lastName": last_name,
                        "reportDate": datetime.now().strftime("%Y-%m-%d"),
                        "service": service_number,
                        "status": "",
                        "training": "",
                        "record status": "Invalid Data ",
                    }
                )
                Response.append(table_data)
                print_the_output_statement(
                    output_text,
                    f"Server ID or Last name is missing for last name {last_name}",
                )
    except PyppeteerTimeoutError as timeout_error:
        print(f"Timeout error: {timeout_error}")
    except pyppeteer.errors.NetworkError as network_error:
        print(f"Network error: {network_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        await browser.close()

    return True, Response
