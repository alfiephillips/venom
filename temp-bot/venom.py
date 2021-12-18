import os
import time
import csv
import dotenv
import asyncio
import requests
import lxml

from smtplib import SMTP

from selenium import webdriver
from selenium.webdriver.common import keys

from concurrent.futures.thread import ThreadPoolExecutor

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup

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
                print("Hello")

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

                if image_filename:
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

class Scalper():
    def __init__(self, url, website="amazon", interval=60, alerts=True, workers=10):
        self.url = url.strip(" ")
        self.website = website
        self.interval = interval
        self.alerts = alerts
        self.driver = webdriver.Chrome(pathname)
        self.workers = workers
        self.executor = ThreadPoolExecutor(workers)

    def get_url(self):
        self.driver.get(self.url)

    def add_task(self, func, loop):
        loop.run_in_executor(self.executor, func, self.url)

class Tracker(Scalper):
    def __init__(self, reciever_name, url, required_price, website="amazon", interval=60, alerts=True):
        self.reciever_name = reciever_name
        self.url = url
        self.required_price = required_price
        self.website = website
        self.interval = interval
        self.alerts = alerts

        self.headers = ({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.5"
        })

        self.product_title = ""
        self.product_price = ""
        self.product_availability = ""
        self.sent_email = False

    def get_product(self):
        if not self.sent_email:
            if self.website.lower() == "amazon":
                webpage = requests.get(self.url, headers=self.headers)
                soup = BeautifulSoup(webpage.content, "lxml")

                try:

                    self.product_title = str(soup.find(
                        "span", attrs={"class": "a-size-large product-title-word-break"}
                    ).get_text().strip(" "))

                    self.product_price = float(soup.find(
                        "span", attrs={"class": 'a-offscreen'}
                        ).get_text().strip("£"))

                    self.product_availability = str(soup.find(
                        "div", attrs={"id": "availability"}
                    ).find(
                        "span", attrs={"class": "a-size-medium a-color-success"}
                    ).get_text().strip(" "))

                
                except AttributeError:
                    price = "N/A"

                if self.required_price >= self.product_price:
                    self.sent_email = True
                    title = "New product available to buy!"
                    message = f"[{self.product_title}] is now available at £{self.product_price}. Its current status remains '{self.product_availability}'\n\nCheck this link to buy: {self.url}"
                    send_email(self.reciever_name, title=title, message=message)
                    print("Email has been sent!")
                    return True

                return False

# loop = asyncio.get_event_loop()

tracker = Tracker("Alfie Phillips", "https://www.amazon.co.uk/dp/B00WWGF4JM/ref=cm_gf_aAN_d_p0_e0_qd0_FpLdDkwNHB0ilz4ceIIx", 55)
tracker.get_product()

# loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop=loop)))