import os
import time
import csv
import dotenv
import asyncio

from smtplib import SMTP

from selenium import webdriver
from selenium.webdriver.common import keys

from concurrent.futures.thread import ThreadPoolExecutor

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

dotenv.load_dotenv()

HOST_ADDRESS = "smtp.gmail.com"
PORT = 587

HOST_EMAIL = os.environ["email"]
HOST_PASSWORD = os.environ["password"]

pathname = os.path.abspath(os.getcwd()) + "/chromedriver.exe"
server = SMTP(host=HOST_ADDRESS, port=PORT)


def setup() -> bool:
    name = str(input("Enter your full name: "))
    email = str(input("Enter your email: "))

    with open("contacts.csv", "a", newline="") as csvfile:
        fields = [name, email]
        writer = csv.writer(csvfile)
        writer.writerow(fields)

    return True

def send_email(reciever_name: str, title="", message="", image_filename=False) -> bool:
    with open("contacts.csv", newline="") as file:
        spamreader = csv.reader(file, delimiter=",")
        for row in spamreader:
            if row[0] == reciever_name:

                reciever_email = row[1]
                
                server.ehlo()
                server.starttls()
                server.ehlo()

                try:
                    server.login(HOST_EMAIL, HOST_PASSWORD)
                except Exception as error:
                    print(f"An Error has occured: {error}")
                    return False

                template = MIMEMultipart()
                template['Subject'] = title
                template["From"] = HOST_EMAIL
                template["To"] = reciever_email

                text = MIMEText(message)
                template.attach(text)

                if image:
                    with open(image, "rb") as file:
                        image_data = f.read()
                        image = MIMEImage(image_data, name=os.path.basename(image_filename))
                        template.attach(image)

                try:
                    server.sendmail(HOST_EMAIL, reciever_email, template.as_string())
                except Exception as error:
                    print(f"An Error has occured: {error}")
                    return False

                server.quit()
                return True

class Venom():
    def __init__(self, url, website="amazon", interval=60, scalp=True, alerts=True, workers=10):
        self.url = url.strip(" ")
        self.interval = interval
        self.scalp = scalp
        self.alerts = alerts
        self.driver = webdriver.Chrome(pathname)
        self.executor = ThreadPoolExecutor(workers)

    def get_url(self):
        self.driver.get(self.url)

    def add_task(self, func, loop):
        loop.run_in_executor(self.executor, func, self.url)

loop = asyncio.get_event_loop()
venom = Venom("https://www.amazon.com/")

venom.add_task(venom.get_url(), loop=loop)
venom.add_task(venom.get_url(), loop=loop)
venom.add_task(venom.get_url(), loop=loop)
venom.add_task(venom.get_url(), loop=loop)
venom.add_task(venom.get_url(), loop=loop)
venom.add_task(venom.get_url(), loop=loop)

loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop=loop)))