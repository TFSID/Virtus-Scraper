import requests
import sys
import time

from icecream import ic

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait




def run_firefox():
    
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.add_argument('-allow-host')
    
    # options.binary_location = ''
    # options.binary_location = '/bin/firefox'
    options.accept_insecure_certs = True
    options.set_preference('geo.prompt.testing', True)
    options.set_preference('geo.prompt.testing.allow', False)
    options.set_preference('javascript.enabled', True)


    # print(options)
    # sys.exit()

    # noinspection PyBroadException
    try:
        driver = webdriver.Firefox(options=options)
        ic(driver)
    except Exception as err:
        # ic(driver)
        sys.exit(f'[!] Failed to run firefox {err}')

    return driver

try:
    with open("ipList.txt", "r") as ipList:
        print("File Opened")
        
        def reqUrl(driver: webdriver,ipList: list):
            for ip in ipList:
                print(ip)
                url = f'https://www.virustotal.com/gui/ip-address/{ip}'
                driver.get(url)
                time.sleep(5)
                # hello = driver.execute_script("console.log('Hello from Selenium!')")
                title = driver.execute_script("return document.title;")
                print(title)
                # aSN = driver.execute_script('document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report > vt-ui-ip-card").shadowRoot.querySelector("div > div.card-body.d-flex > div > div.hstack.gap-4 > div.vstack.gap-2.align-self-center.text-truncate.me-auto > div:nth-child(2) > a")')
                i = 0
                while i < 10:
                    try:
                        aSNumber = 'document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report > vt-ui-ip-card").shadowRoot.querySelector("div > div.card-body.d-flex > div > div.hstack.gap-4 > div.vstack.gap-2.align-self-center.text-truncate.me-auto > div:nth-child(2) > a")'
                        aSName = 'document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report > vt-ui-ip-card").shadowRoot.querySelector("div > div.card-body.d-flex > div > div.hstack.gap-4 > div.vstack.gap-2.align-self-center.text-truncate.me-auto > div:nth-child(2) > span > a")'
                        country = 'document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report > vt-ui-ip-card").shadowRoot.querySelector("#country")'
                        cIDR = 'document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report > vt-ui-ip-card").shadowRoot.querySelector("div > div.card-body.d-flex > div > div.hstack.gap-4 > div.vstack.gap-2.align-self-center.text-truncate.me-auto > div:nth-child(1) > a")'
                        score = 'document.querySelector("#view-container > ip-address-view").shadowRoot.querySelector("#report").shadowRoot.querySelector("div > div.row.mb-4.d-none.d-lg-flex > div.col-auto > vt-ui-detections-widget").shadowRoot.querySelector("div > div > div.positives")'
                        getList = [aSNumber, aSName, cIDR, country, score]
                        fetchList = 0
                        while fetchList < len(getList):
                            try:
                                # Use JavaScript to find the element
                                js_selector = getList[fetchList]
                                element = driver.execute_script(f'return {js_selector};')
                                stringList =  ["ASN","AS Name", "CIDR","Country","Risk Level"]
                                # Interact with the element if it is found
                                if element:
                                    print(f"[+] found {stringList[fetchList]}")
                                    print(f"Element found using JavaScript: {element.text}")
                                else:
                                    print("Element not found using JavaScript")
                                fetchList += 1
                            except Exception as err:
                                print(f"Error using JavaScript: {err}")
                                print('[!] Retrying.....')
                                i += 1
                        break
                    except Exception as err:
                        print(err)
                        # print(driver.page_source)
                        with open('check.html','w', encoding="utf-8") as html:
                            html.write(driver.page_source)
                        print('[!] Failed get element [@id="report"]')
                        print('[!] Retrying.....')
                        i += 1
                time.sleep(5)
                with open('check.html','w', encoding="utf-8") as html:
                    html.write(driver.page_source)
        driver = run_firefox()
        reqUrl(driver, ipList)
        driver.quit()
        print("Task Completed")
        

except Exception as err:
    print("File Not Opened",err)


# r = requests.get('https://www.virustotal.com/gui/ip-address/206.189.149.76')
# r.status_code
# print()
# with open('check2.html','w', encoding="utf-8") as html:
#         html.write(r.text)