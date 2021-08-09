
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import json


ENDPOINT = "things.ubidots.com"
DEVICE_LABEL = "lenovo"
TOKEN = "" # Your Ubidots token
STATUS_LABEL = "last_status"

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

def get_last_status(url=ENDPOINT, device=DEVICE_LABEL, token=TOKEN, var=STATUS_LABEL):
    base_url = 'https://things.ubidots.com/api/v1.6/devices/%s/%s/values'%(device, var)
    try:
        r = requests.get(base_url + '?token=%s&page_size=%i'%(token,1), timeout=20)
        return r.json()
    except Exception as e:
        print(e)
        return {'error': 'Request failed or timed out'}


def main():
    url = "https://ovp.lenovo.com/lenovo-ovp-new/public/ordersearch?appId=1ea53a968e157ecfe69bda62621c5074dbb54e0ae7c86c6a0d2164ad17ccca4348ca18ca40534d35fee41930cb8bcf6bfd4d0d129de6048f1452714253a76505&orderNumber=3f349768d3b3914ded1eaa35901d547547097ea87e52562a8244ec8f7c2e99046137a17bf93f3dc0f4f6f079b87729d5971f1512d025eb3efb97aa7dd43c8e10&email=9e00995114c7910ee2d0a688562a5b7638626a58f994467198bfcf3894fc8202225cd4dcb0b06fed47ecaf54fa62f623a06af57b5b80ab965e81c8f10a456dbc&lang=es_CL&locale=es_CL"


    url_headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    response = requests.get(url, headers=url_headers)
    html_text = response.text
    print(type(html_text))
    print(len(html_text))

    soup = BeautifulSoup(html_text, "lxml")
    estados = soup.find_all('div', class_="col-xs-4")
    print(f'Hay {len(estados)} estados disponibles')
    for idx,estado in enumerate(estados):
        try:
            stat = estado.font["style"] #string, 'font-weight: bold; color: black;'
            if stat == 'font-weight: bold; color: black;':
                new_status = idx
            else:
                print("HOLACHAO")
        except:
            stat = ''


    # new_Status puede ser 0,1,2. Si es mayor a 0, entonces avanzó >:3
    nombres_estados = ["Ordered", "Shipping", "Arrival"]
    print(f'La compra se encuentra en el estado "{nombres_estados[new_status]}"')
    pancho = {}
    pancho["last_status"] = new_status
    last_status = int(get_last_status()['results'][0]['value'])
    print(last_status)

    if new_status != last_status:
        pancho['notify']=1
        post_var(pancho)
        time.sleep(10)
        post_var({'notify': 0})



if __name__=="__main__":
    try:
        main()
    except:
        print("Error except main")