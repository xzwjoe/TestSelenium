from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import csv



class Run:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.recordUrl = "http://test"
        print("start")

    def writeText(self, text):
        file_name = os.path.join(os.getcwd(),"log.txt")
        now = datetime.now()
        f = open(file_name, 'a')
        f.writelines(str(now) + ": " + text + "\n")
        f.close()
    
    def sendMail(self):
        sendAddress = 'xzwjoe@gmail.com'
        password = 'lktqwcaeossmjbbs'

        subject = 'GET!'
        bodyText = 'GET! ' + self.recordUrl
        fromAddress = 'xzwjoe@gmail.com'
        toAddress = ['xzwjoe@gmail.com']

        # SMTPサーバに接続
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.starttls()
        smtpobj.login(sendAddress, password)

        # メール作成
        msg = MIMEText(bodyText)
        msg['Subject'] = subject
        msg['From'] = fromAddress
        msg['To'] = ", ".join(toAddress)
        msg['Date'] = formatdate()

        # 作成したメールを送信
        smtpobj.send_message(msg)
        print("mail send")
        smtpobj.close()

    def isElementExistId(self, element):
        browser = self.driver
        try:
            ret = browser.find_element(By.ID, element)
            return ret

        except:
            return None
    
    def isElementExist(self, element):
        browser = self.driver
        try:
            ret = browser.find_element(By.XPATH, element)
            return ret
        except:
            return None

    def isElementExistTag(self, element):
        browser = self.driver
        try:
            ret = browser.find_elements(By.TAG_NAME, element)
            return ret
        except:
            return None

    #ログイン処理
    def login(self):
        wesite_url = "https://www.hermes.com/jp/ja/"

        browser = self.driver
        browser.get(wesite_url)

        #アカウントタグをクリック
        account_button = self.isElementExist("//button[@aria-controls='tray-account']")
        account_button.click()
        time.sleep(2)
        login_email = self.isElementExistId("login-email")

        #wait 10s for display textbox
        count = 0
        while not login_email.is_displayed() :
            count += 1
            if count > 10:
                break
            time.sleep(1)

        login_email.click()
        #TODO
        login_email.send_keys("")
        login_password = self.isElementExistId("login-password")
        time.sleep(3)
        login_password.click()
        #TODO
        login_password.send_keys("")
        time.sleep(2)
        login_button = self.isElementExistId("loginButton")
        login_button.click()
        time.sleep(10)

    #バッグを探す
    def find(self):
        url = "https://www.hermes.com/jp/ja/category/women/bags-and-small-leather-goods/bags-and-clutches/#|"
        #url = "file:///C:/Users/xzwta/Downloads/hermes/tt.html"

        #pattern1, pattern2, pattern3 = "ピコタン", "ロック", "18"
        pattern1, pattern2, pattern3 = "ヴェルー", "チェーン", "ミニ"
        target_bag_link = None

        browser = self.driver
        browser.get(url)
        time.sleep(5)
        result = browser.find_elements(By.CLASS_NAME, "product-item-name")

        for r in result:
            innerText = r.get_attribute("innerText")
            if pattern1 in innerText and pattern2 in innerText and pattern3 in innerText:
                self.writeText("found!!")
                r.click()
                return True

        return False

    #カートに入れる
    def addToCart(self):
        browser = self.driver
        #wait 20s
        count = 0
        while "product" not in browser.current_url:
            count += 1
            if count > 20:
                break
            time.sleep(1)
        #URLを記録
        self.writeText(browser.current_url)
        self.recordUrl = browser.current_url
        #Add to cartボタン
        button = self.isElementExist("//button[@name='add-to-cart']")
        if button.is_enabled():
            button.click()
        else:
            self.writeText("too slow...")

        time.sleep(2)
        #ショッピングバッグを見るボタンが表示されたら
        cartbutton = self.isElementExist("//button[@name='add-to-cart']")
        if cartbutton.is_displayed():
            #メール送信
            self.sendMail()

    def collectInfo(self):
        browser = self.driver
        url = "https://www.hermes.com/jp/ja/category/women/bags-and-small-leather-goods/bags-and-clutches/#|"
        browser.get(url)
        time.sleep(10)

        #Read Product csv
        dict_from_csv = {}
        file_name = os.path.join(os.getcwd(),"products.txt")
        if os.path.isfile(file_name):
            with open(file_name, mode='r') as inp:
                reader = csv.reader(inp)
                dict_from_csv = {rows[0]:rows[1] for rows in reader}

        #get products
        list = browser.find_elements(By.XPATH, "//div[@class='product-item']")
        for l in list:
            name = l.find_element(By.CLASS_NAME, "product-item-name").get_attribute("innerText")
            link = l.find_element(By.TAG_NAME, "a").get_property("href")
            #write to csv
            if name not in dict_from_csv.keys():
                with open(file_name, 'a', newline='') as f:
                    f.writelines(name + "," + link + "\n")



        #file_name = os.path.join(os.getcwd(),"product.csv")
        #f = open(file_name, 'a')
        #f.writelines("\n")


        


run = Run()
run.collectInfo()
#run.login()
found = False
while not found:
    found = run.find()
    if found:
        break
    time.sleep(300)
if found:
    run.addToCart()
time.sleep(300)