import requests
from bs4 import BeautifulSoup
import bs4
import pymysql

def getHtmlText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr,bs4.element.Tag):
            tds=tr('td')
            ulist.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string])

def printUnivList(ulist,num):
    tplt="{0:^10}\t{1:{4}^10}\t{2:^10}\t{3:^10}"
    print(tplt.format("排名","学校名称","省市","总分",chr(12288)))
    for i in range(num):
        u=ulist[i]
        print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))

def saveUnivList(ulist,num):
        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='sys',charset='utf8')
        cur=conn.cursor()

        data=[]
        for i in range(num):
                data.append(ulist[i])

        sql="insert into tb_university(排名,学校名称,省市,总分) values(%s,%s,%s,%s)"
        try:
                cur.executemany(sql,data)
                conn.commit()
        except:
                conn.rollback()
        
        cur.close()
        conn.close()
        print("数据保存成功")
        

def main():
    uinfo=[]
    url='http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html'
    html=getHtmlText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo,100)
    saveUnivList(uinfo,100)
main()