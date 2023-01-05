from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

from loguru import logger


from brownie_request import brownie_request


url = ""
profile = None
options = None


def init_browser():
    global url, profile, options

    logger.info("Setting up firefox for the bot...")
    url = "https://tellslimchickens.smg.com/"

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)  # Start in private mode
    logger.debug("Set firefox to use private browsing")

    options = Options()
    options.add_argument("--headless")
    logger.debug("Set firefox to start in headless mode")
    logger.success("Loaded profiles and settings for the browser!")


def get_brownie_code(request: brownie_request):
    logger.info("Beginning survey now...")
    if len(str(request.store_number)) != 4:
        logger.error("Store number is not 4 digits!")
        return
    if len(str(request.order_id)) < 10:
        logger.error(f"Order if is not greater than 10 digits! Was passed a order id of '{request.order_id}' which has a length of {len(request.order_id)}")
        return

    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(url)
    logger.debug("Opened survey!")
    logger.debug("Waiting for page to load...")

    # Input details
    store_number_input = driver.find_element(By.NAME, value="InputStoreNum")
    store_number_input.send_keys(request.store_number)
    logger.debug("Entered the store number")

    driver.find_element(By.CLASS_NAME, value="ui-datepicker-trigger").click()  # Open calender widget
    driver.find_element(By.LINK_TEXT, value=str(request.date.split("/")[1])).click()
    logger.debug("Entered the date")

    split_time = request.time.split(":")
    hour = split_time[0]
    minute = split_time[1].split(" ")[0]
    meridian = split_time[1].split(" ")[1].upper()
    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute
    hour_input = Select(driver.find_element(By.NAME, value="InputHour"))
    minute_input = Select(driver.find_element(By.NAME, value="InputMinute"))
    meridian_input = Select(driver.find_element(By.NAME, value="InputMeridian"))
    hour_input.select_by_value(hour)
    minute_input.select_by_value(minute)
    meridian_input.select_by_value(meridian)
    order_id_input = driver.find_element(By.NAME, value="InputCheckNum")
    order_id_input.send_keys(request.order_id)
    logger.debug("Inputted time")

    # Submit
    driver.find_element(By.NAME, value="NextButton").click()
    logger.debug("Hit next button")

    highly_satisfied_button = ""
    while highly_satisfied_button == "":
        highly_satisfied_button = driver.find_element(By.CLASS_NAME, value="radioSimpleInput")
    highly_satisfied_button.click()
    logger.debug("Hit the highly satisfied button")

    driver.find_element(By.ID, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value=f"//label[contains(text(), '{request.receipt_location}')]/preceding-sibling::span[1]").click()
    logger.debug("Entered receipt location")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    buttons = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlySatisfiedNeitherDESC5"]')
    for button in buttons:
        button.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
        logger.debug("Clicked a highly satisfied button")
    # Submit
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    buttons = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlySatisfiedNeitherDESC5"]')
    for button in buttons:
        button.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
        logger.debug("Clicked a highly satisfied button")
    # Submit
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    # No problems had
    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    logger.debug("Clicked a highly satisfied button")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    # Likelihood
    elements = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlyLikelyDESC5"]')
    for element in elements:
        element.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
        logger.debug("Hit highly likely button")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    da_paragraph = driver.find_element(By.NAME, value="S000024")
    da_paragraph.send_keys("I had an excellent time at Slim Chicken's. The food was wonderful, and it was just the right temperature. When I ordered the staff were very polite and made the experience all the more easy.")
    logger.debug("Entered the looooooong paragraph")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    elements = driver.find_elements(By.XPATH, value='//td[@aria-describedby="YesNoASC1"]')
    for element in elements:
        element.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
        logger.debug("Hit YES button")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC1"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME,value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value=f"//label[contains(text(), 'Four or more')]/preceding-sibling::span[1]").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value=f"//label[contains(text(), 'Convenience of location')]/preceding-sibling::span[1]").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    age = Select(driver.find_element(By.NAME, value="R000035"))
    age.select_by_value("2")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()
    logger.debug("Hit next button")

    code = driver.find_element(By.CLASS_NAME, value="ValCode").text.split(": ")[1]
    request.code = f"screenshots/{code}.png"
    logger.success("Retrieved the code!")

    driver.save_screenshot(f"screenshots/{code}.png")

    driver.close()
    logger.info("Closed the browser...Exiting session!")
