from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


async def get_brownie(store_number: str, date: str, time: str, order_id: str, receipt_location: str, request_id: int = 0):
    if len(str(store_number)) != 4:
        return
    if len(str(order_id)) != 10:
        return

    url = "https://tellslimchickens.smg.com/"
    driver = webdriver.Firefox()
    driver.get(url)

    # Input details
    store_number_input = driver.find_element(By.NAME, value="InputStoreNum")
    store_number_input.send_keys(store_number)

    driver.find_element(By.CLASS_NAME, value="ui-datepicker-trigger").click()  # Open calender widget
    driver.find_element(By.LINK_TEXT, value=str(date.split("/")[1])).click()

    split_time = time.split(":")
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
    order_id_input.send_keys(order_id)
    # Submit
    driver.find_element(By.NAME, value="NextButton").click()

    highly_satisfied_button = ""
    while highly_satisfied_button == "":
        highly_satisfied_button = driver.find_element(By.CLASS_NAME, value="radioSimpleInput")
    highly_satisfied_button.click()
    driver.find_element(By.ID, value="NextButton").click()

    driver.find_element(By.XPATH, value=f"//label[contains(text(), '{receipt_location}')]/preceding-sibling::span[1]").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    buttons = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlySatisfiedNeitherDESC5"]')
    for button in buttons:
        button.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    # Submit
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    buttons = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlySatisfiedNeitherDESC5"]')
    for button in buttons:
        button.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
        # Submit
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    # No problems had
    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    # Likelihood
    elements = driver.find_elements(By.XPATH, value='//td[@aria-describedby="HighlyLikelyDESC5"]')
    for element in elements:
        element.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    da_paragraph = driver.find_element(By.NAME, value="S000024")
    da_paragraph.send_keys("I had an excellent time at Slim Chicken's. The food was wonderful, and it was just the right temperature. When I ordered the staff were very polite and made the experience all the more easy.")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    elements = driver.find_elements(By.XPATH, value='//td[@aria-describedby="YesNoASC1"]')
    for element in elements:
        element.find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC1"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME,value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    driver.find_element(By.XPATH, value=f"//label[contains(text(), 'Four or more')]/preceding-sibling::span[1]").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    driver.find_element(By.XPATH, value=f"//label[contains(text(), 'Convenience of location')]/preceding-sibling::span[1]").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    age = Select(driver.find_element(By.NAME, value="R000035"))
    age.select_by_value("2")
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    driver.find_element(By.XPATH, value='//td[@aria-describedby="YesNoASC2"]').find_element(By.CLASS_NAME, value="radioSimpleInput").click()
    driver.find_element(By.CLASS_NAME, value="NextButton").click()

    code = driver.find_element(By.CLASS_NAME, value="ValCode").text.split(": ")[1]
    with open("codes.txt", "w") as codes:
        codes.write(f"{request_id}:{code}")


if __name__ == "__main__":
    get_brownie("0000", "10/12/1997", "1:54 PM", "0000000000", "Drive thru", "TEST")
