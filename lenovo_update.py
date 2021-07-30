
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time


ENDPOINT = "things.ubidots.com"
DEVICE_LABEL = "lenovo"
TOKEN = "" # Ubidots Token
DELAY = 1800  # Update every 1/2 hour



def post_var(payload, url=ENDPOINT, device=DEVICE_LABEL, token=TOKEN):
    try:
        url = "http://{}/api/v1.6/devices/{}".format(url, device)
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

        attempts = 0
        status_code = 400

        while status_code >= 400 and attempts < 5:
            print("[INFO] Sending data, attempt number: {}".format(attempts))
            req = requests.post(url=url, headers=headers,
                                json=payload)
            status_code = req.status_code
            attempts += 1
            time.sleep(1)

        print("[INFO] Results:")
        print(req.text)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))





driver = webdriver.Chrome()
url = "https://www.lenovo.com/cl/es/laptops/laptops-legion/legion-5-series/c/legion-5-series"
# html_text = requests.get(url) was not allowed, error 403

driver.get(url)
html_text = driver.page_source
driver.close()

soup = BeautifulSoup(html_text, 'lxml')
computers = soup.find_all('li', class_ = "product isVisible")

# print(f'Hay {len(computers)} computadores')
models = {}
for computer in computers:
    name = computer.find('h3', class_ = "seriesListings-title").text[1:-1]
    try:
        price = computer.find('dl', class_ = "cta-price").dd.text
        price = ''.join(price[1:].split('.'))
    except:
        price = 0
    print(name, price)
    models[name] = price


notify = False
print(len(models))
if len(models) > 3:
    notify = True

for model in models:
    print(model, models[model])
    if '6ta' in model and models[model]!=0:
        notify=True
print(notify)

#notify=True # for debugging

if notify:
    models['notify']=1
    post_var(models)
