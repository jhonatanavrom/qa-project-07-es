import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(self):
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    import json
    import time
    from selenium.common import WebDriverException

    code = None
    for i in range(20):
        try:
            logs = [log["message"] for log in self.driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = self.driver.execute_cdp_cmd('Network.getResponseBody',
                                                   {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue

        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")

        return code


class UrbanRoutesPage:
    element = None
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    select_taxi_button = (By.XPATH, ".//div[@class='results-text']//button[contains(text(),'Pedir un taxi')]")
    select_comfort_button = (By.XPATH, ".//div[@class='tariff-cards']//div[contains(text(), 'Comfort')]")
    select_phone_field = (By.XPATH, ".//div[@class='form']//div[@class='np-text']")
    input_phone_field = (By.XPATH, ".//div[@class='number-picker open']//input[@id='phone']")
    select_next_phone_button = (By.XPATH, ".//div[@class='buttons']//button[contains(text(), 'Siguiente')]")
    input_sms_code = (By.XPATH, ".//div[@class='input-container']//input[@id='code']")
    submit_phone_number = (By.XPATH, ".//div[@class='buttons']//button[contains(text(), 'Confirmar')]")
    select_payment_method = (By.XPATH, ".//div[@class='pp-value']//div[@class='pp-value-text']")
    add_new_card = (By.XPATH, ".//div[@class='modal']//div[@class='pp-plus-container']")
    write_card_number = (By.XPATH, ".//div[@class='card-number-input']//input[@id='number']")
    write_cvv_card = (By.XPATH, ".//div[@class='card-code-input']//input[@id='code']")
    activate_submit_card_button = (By.XPATH, ".//div[@class='card-wrapper']//div[@class='pp-separator']")
    submit_card_information = (By.XPATH, ".//div[@class='pp-buttons']//button[contains(text(), 'Agregar')]")
    close_payment_window = (By.XPATH, ".//div[@class='payment-picker open']//button[@class='close-button section-close']")
    write_message_to_driver = (By.XPATH, ".//div[@class='input-container']//input[@id='comment']")
    turn_switch_blanket = (By.XPATH, ".//div[@class='r-sw']//div[@class='switch']")
    add_ice_cream = (By.XPATH, ".//div[@class='r-counter']//div[@class='counter-plus']")
    count_ice_cream_value = (By.XPATH, ".//div[@class='r-counter']//div[@class='counter-value']")
    request_taxi_button = (By.XPATH, ".//div[@class='smart-button-wrapper']//button[@class='smart-button']")
    wait_modal_taxi = (By.XPATH, ".//div[@class='order shown']//div[@class='order-body']")


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        time.sleep(2)
        self.set_from(from_address)
        self.set_to(to_address)

    def request_taxi_comfort(self):
        time.sleep(2)
        self.driver.find_element(*self.select_taxi_button).click()
        self.driver.find_element(*self.select_comfort_button).click()

    def get_comfort_card(self):
        return self.driver.find_element(*self.select_comfort_button).is_enabled()

    def enter_phone_number(self, phone_number):
        self.driver.find_element(*self.select_phone_field).click()
        self.driver.find_element(*self.input_phone_field).send_keys(phone_number)
        self.driver.find_element(*self.select_next_phone_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.select_phone_field).text

    def confirm_phone_number(self, sms_code):
        self.driver.find_element(*self.input_sms_code).send_keys(sms_code)
        self.driver.find_element(*self.submit_phone_number).click()

    def add_payment_method(self, card_number, cvv_code):
        self.driver.find_element(*self.select_payment_method).click()
        self.driver.find_element(*self.add_new_card).click()
        #
        self.driver.find_element(*self.write_card_number).send_keys(card_number)
        self.driver.find_element(*self.write_cvv_card).send_keys(cvv_code)
        self.driver.find_element(*self.write_cvv_card).send_keys(Keys.TAB)
        self.driver.find_element(*self.submit_card_information).click()
        self.driver.find_element(*self.close_payment_window).click()

    def get_payment_method(self):
        return self.driver.find_element(*self.select_payment_method).text

    def send_comment_to_driver(self, comment):
        self.driver.find_element(*self.write_message_to_driver).send_keys(comment)

    def get_comment_driver(self):
        return self.driver.find_element(*self.write_message_to_driver).get_property('value')

    def select_blankets(self):
        self.driver.find_element(*self.turn_switch_blanket).click()

    def get_blankets_button_status(self):
        return self.driver.find_element(*self.turn_switch_blanket).is_enabled()

    def select_ice_cream(self, items):
        for i in range(items):
            self.driver.find_element(*self.add_ice_cream).click()

    def get_ice_cream_items(self):
        return self.driver.find_element(*self.count_ice_cream_value).text

    def click_to_request_taxi(self):
        self.driver.find_element(*self.request_taxi_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located(UrbanRoutesPage.wait_modal_taxi))
        time.sleep(5)


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        #no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        chrome_options = ChromeOptions()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_request_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.request_taxi_comfort()
        assert routes_page.get_comfort_card() == True

    def test_enter_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = data.phone_number
        routes_page.enter_phone_number(phone_number)
        sms_code = retrieve_phone_code(self)
        routes_page.confirm_phone_number(sms_code)
        assert routes_page.get_phone_number() == phone_number


    def test_add_payment_method(self):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        cvv_code = data.card_code
        payment_method = data.payment
        routes_page.add_payment_method(card_number, cvv_code)
        assert routes_page.get_payment_method() == payment_method

    def test_send_comment_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        comment = data.message_for_driver
        routes_page.send_comment_to_driver(comment)
        assert routes_page.get_comment_driver() == comment

    def test_select_blankets(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_blankets()
        assert routes_page.get_blankets_button_status() == True

    def test_select_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        items = data.ice_cream_items
        routes_page.select_ice_cream(items)
        assert routes_page.get_ice_cream_items() == str(items)

    def test_click_to_request_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_to_request_taxi()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
