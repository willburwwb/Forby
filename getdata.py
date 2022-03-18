from typing import List, Any
from urllib import request
from bs4 import BeautifulSoup
import pymysql


class myData(object):
    def __init__(self, the_page):
        self.author_list = []
        self.title_list = []
        self.abstract_list = []
        self.subjects_list = []
        self.date_list = []
        self.link_list = []
        self.the_page = the_page
        self.db = pymysql.connect(host="localhost", port=3308, user="root", password="wwb20030526", db="test")
        self.cursor = self.db.cursor()

    def askurl(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
        }
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        return res.read().decode("utf-8")

    def askdate(self, now_abstract):
        url = "https://arxiv.org/abs/" + now_abstract[6:]
        bs = BeautifulSoup(self.askurl(url), "html.parser")
        date = bs.select("div.dateline")
        date_text = date[0].text.replace('\n', '').strip(' ')
        self.date_list.append(date_text[11:-1])

    def SSelect(self, name, ask_name):
        sql = f"""
                select {name} from hust
                where {name} REGEXP '{ask_name}'
           """
        self.cursor.execute(sql)
        if len(self.cursor.fetchall()):
            return 1
        else:
            return 0

    def getdata(self, url):
        # 用bs4库 同时将页面内容解析称html格式
        bs = BeautifulSoup(self.askurl(url), "html.parser")
        # 个人认为bs比正则表达式简单一些qaq,同时可以看官方手册很全
        title = bs.select("div#dlpage > dl > dd > div > div.list-title.mathjax")
        author = bs.select("dd > div.meta > div.list-authors")
        abstract = bs.select('div#dlpage> dl > dt > span >a[title="Abstract"]')
        subjects = bs.select("dd > div.meta > div.list-subjects > span.primary-subject")
        link = bs.select('div#dlpage> dl > dt > span >a[title="Download PDF"]')
        for i in range(0, int(self.the_page)):
            self.title_list.append(title[i].text.strip('\n')[7:])
            self.author_list.append(author[i].text[9:])
            self.author_list[i] = self.author_list[i].replace('\n', '')
            self.abstract_list.append(abstract[i].text)
            self.subjects_list.append(subjects[i].text)
            self.link_list.append("https://arxiv.org" + link[i].get('href'))
            if self.SSelect('hust_link', self.link_list[i]) == 1:
                self.the_page = i - 1
                break
            # 获取日期稍微麻烦一点
            self.askdate(self.abstract_list[i])
            print("第%d篇论文爬取完毕" % (i + 1))

    def Insert(self, id):
        sql = f"""
            insert into hust(
               hust_title, hust_author, hust_date, hust_subject, hust_link
            )
            values (
                '{self.title_list[id]}','{self.author_list[id]}','{self.date_list[id]}','{self.subjects_list[id]}','{self.link_list[id]}'
            )
        """
        # 千万千万千万要注意！！！！{字符}外面加上单引号，别问我怎么知道的。
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print(f"第{id}条数据未成功插入")
            self.db.rollback()
        else:
            print(f"成功插入第{id}条数据")

    def askMysql(self):
        for i in range(0, int(self.the_page)):
            self.Insert(i)
