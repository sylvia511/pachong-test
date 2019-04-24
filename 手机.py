from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pymysql

class MySpider():
    def StartUp(self,url,key):    
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver=webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)
        keyInput=self.driver.find_element_by_id("key")
        keyInput.send_keys(key)
        keyInput.send_keys(Keys.ENTER)

    def processSpider(self):
        time.sleep(1)
        print(self.driver.current_url)

        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='sys',charset='utf8')
        cur=conn.cursor()
        
        lis=self.driver.find_elements_by_xpath("//div[@id='J_goodsList']//li[@class='gl-item']")
        for li in lis:
            price=li.find_element_by_xpath(".//div[@class='p-price']//i").text
            name=li.find_element_by_xpath(".//div[@class='p-name p-name-type-2']//em").text
            mark=self.driver.find_element_by_css_selector('a.curr-shop')
            mark=mark.text
            print(name,mark,price)

            sql="insert into phones(mName,mMark,mPrice) values(%s,%s,%s)"
            cur.execute(sql,(name,mark,price))
            conn.commit()

            try:
                self.driver.find_element_by_xpath(".//span[@class='p-num']//a[@class='pn-prev disabled']")
            except:
                nextPage=self.driver.find_element_by_xpath(".//span[@class='p-num']//a[@class='pn-next']")
                nextPage.click()
                self.processSpider()
    
    def executeSpider(self,url,key):
        starttime=datetime.datetime.now()
        print("Spider starting......")
        self.StartUp(url,key)
        self.processSpider()
        endtime=datetime.datetime.now()
        elapsed=(endtime-starttime).seconds
        print("Total",elapsed,"seconds elapsed")

url='http://www.jd.com'
spider=MySpider()
spider.executeSpider(url,"vivox23全息幻彩")