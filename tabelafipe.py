from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests

class WhatsAppBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://web.whatsapp.com")
        self.wait = WebDriverWait(self.driver, 20)
        input("Scan QR code and press Enter...")

    def check_new_messages(self):
        try:
            unread = self.wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 'span[data-testid="icon-unread-count"]'
            )))
            for msg in unread:
                msg.click()
                time.sleep(1)
                self.process_message()
        except:
            pass

    def process_message(self):
        messages = self.driver.find_elements(By.CSS_SELECTOR, 'div.message-in')
        if messages:
            last_message = messages[-1].text.strip()
            
            if last_message.startswith('/fipe'):
                try:
                    codigo_fipe = last_message.split()[1]
                    fipe_data = self.consultar_fipe(codigo_fipe)
                    self.send_message(self.format_fipe_data(fipe_data))
                except:
                    self.send_message("Erro: Use /fipe CÓDIGO_FIPE")

    def consultar_fipe(self, codigo):
        url = f"https://brasilapi.com.br/api/fipe/preco/v1/{codigo}"
        response = requests.get(url)
        return response.json()

    def format_fipe_data(self, data):
        return (f"*Consulta FIPE*\n"
                f"Marca: {data['marca']}\n"
                f"Modelo: {data['modelo']}\n"
                f"Ano: {data['anoModelo']}\n"
                f"Valor: {data['valor']}\n"
                f"Combustível: {data['combustivel']}")

    def send_message(self, message):
        input_box = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'div[contenteditable="true"]'
        )))
        input_box.send_keys(message + Keys.ENTER)

    def start(self):
        print("Bot iniciado! Monitorando mensagens...")
        while True:
            self.check_new_messages()
            time.sleep(3)

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.start()