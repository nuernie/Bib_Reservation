from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time

# Python script for auto library check in
# author Patrick Nuernberger
# TODO name minuten einstellung als UserInput umschreiben
# TODO Code besser kapseln / Funktionen
# TODO Error-Handling noch ergänzen

full_name = "your name"
tum_user = "username"
mail_adr = "your email"
minutes_refr = 10


merk_list = []
s = Service(r"C:\Users\Paddy\Desktop\Hobby\Coding\Bib-Reservation\driver\chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get("https://www.ub.tum.de/arbeitsplatz-reservieren")
chrome_options = Options()
chrome_options.add_experimental_option("detach", False)


# Implementation Logic
# error handling betreiben falls ein Element nicht gefundne wird!
# tr = row
# td = column


while(1):
    # check clock
    end_of_day_datetime = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    now = datetime.now()
    past = end_of_day_datetime - timedelta(minutes=minutes_refr)
    future = end_of_day_datetime + timedelta(minutes=minutes_refr)

    if(past <= now and now <= future):
        data = driver.find_elements(By.XPATH, '//*[@id="block-system-main"]/div/div/div[2]/table/tbody/tr')
        # einfach überall einen Platz reservieren
        # rufe die ganzen Tabs auf
        for e1 in data :
            # print(e1.text)
            if ("Zur Reservierung" in e1.text) and (e1.find_element(By.TAG_NAME, 'td').text == "Stammgelände") and not(e1.text in merk_list):
                merk_list.append(e1.text)
                website = e1.find_element(By.TAG_NAME,'a').get_attribute('href')
                ex_str = "window.open('"+str(website)+"')"
                driver.execute_script(ex_str)
            else:
                print("this elements are not allowed!")

        # fuelle formular in einzelnen tabs aus
        for chld in  driver.window_handles[1:]:
            driver.switch_to.window(chld)

            name = driver.find_element(By.XPATH, '//*[@id="edit-field-tn-name-und-0-value"]')
            name.send_keys(full_name)
            mail = driver.find_element(By.XPATH, '//*[@id="edit-anon-mail"]')
            mail.send_keys(mail_adr)
            driver.find_element(By.XPATH, '//*[@id="edit-field-stud-ma-und"]/div[1]/label').click()
            tum_acc = driver.find_element(By.XPATH, '//*[@id="edit-field-tum-kennung-und-0-value"]')
            tum_acc.send_keys(tum_user)
            driver.find_element(By.XPATH, '//*[@id="edit-field-benutzungsrichtlinien"]/div').click()
            driver.find_element(By.XPATH, '//*[@id="edit-field-datenschutzerklaerung"]/div/label/span').click()
            ##### click anmeldung
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="edit-submit"]').click()
            ######
            driver.close()

        # referenziere driver erneut
        chld = driver.window_handles[0]
        driver.switch_to.window(chld)

        # warte 2 sec wegen ddos dann refresh und check auf neue Elemente
        time.sleep(2)
        driver.refresh()
        print(merk_list)














