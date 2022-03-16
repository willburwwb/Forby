from urllib import request
import requests
from bs4 import BeautifulSoup
import pymysql
import abc

# 操作网页url。打开读取url。
def askurl(url):
    # 这里需要模拟一下用户代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
    }
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    return res.read().decode("utf-8")


author_list = []
title_list = []
abstract_list = []
subjects_list = []
date_list = []
link_list = []
the_page = 0
baseurl = "https://arxiv.org/list/cs.AI/pastweek?skip=0"


def askdate(now_abstract):
    url = "https://arxiv.org/abs/" + now_abstract[6:]
    bs = BeautifulSoup(askurl(url), "html.parser")
    date = bs.select("div.dateline")
    date_text = date[0].text.replace('\n', '').strip(' ')
    date_list.append(date_text[11:-1])

downloadurl = r"D:\file\HustLC\Artificial Intelligence\AI"

def getdata(url):
    # 用bs4库 同时将页面内容解析称html格式
    bs = BeautifulSoup(askurl(url), "html.parser")
    # 个人认为bs比正则表达式简单一些qaq,同时可以看官方手册很全
    title = bs.select("div#dlpage > dl > dd > div > div.list-title.mathjax")
    author = bs.select("dd > div.meta > div.list-authors")
    abstract = bs.select('div#dlpage> dl > dt > span >a[title="Abstract"]')
    subjects = bs.select("dd > div.meta > div.list-subjects > span.primary-subject")
    link = bs.select('div#dlpage> dl > dt > span >a[title="Download PDF"]')
    # print(url)
    for i in range(0, int(the_page)):
        title_list.append(title[i].text.strip('\n')[7:])
        author_list.append(author[i].text[9:])
        author_list[i] = author_list[i].replace('\n', '')
        abstract_list.append(abstract[i].text)
        subjects_list.append(subjects[i].text)
        link_list.append("https://arxiv.org" + link[i].get('href'))
        '''
        # 下载文件至制定的文件夹,先获取pdf链接，然后get其中内容，最后读入到制定文件夹中
        print(link_list[i])
        download_pdf = requests.get(link_list[i])
        with open(downloadurl + str(i) + ".pdf", mode='wb') as f:
            # print("开始爬",i)
            f.write(download_pdf.content)
            # print("爬完了")
        '''
        # 获取日期稍微麻烦一点
        askdate(abstract_list[i])
        print("第%d篇论文爬取完毕" % (i + 1))

db = pymysql.connect(host="localhost", port=3308, user="root", password="wwb20030526", db="test")
sql = ""
cursor = db.cursor()
def Select(name,askname):
    sql=f"""
        select * from hust
        where {name} REGEXP '.*{askname}.*'
    """
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except:
        import traceback
        traceback.print_exc()
    else:
        print("查找成功")
def Insert(id):
    sql = f"""
        insert into hust(
           hust_title, hust_author, hust_date, hust_subject, hust_link
        )
        values (
            '{title_list[i]}','{author_list[i]}','{date_list[i]}','{subjects_list[i]}','{link_list[i]}'
        )
    """
    # 千万千万千万要注意！！！！{字符}外面加上单引号，别问我怎么知道的。
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(f"第{i}条数据未成功插入")
        db.rollback()
    else:
        print(f"成功插入第{id}条数据")

def Update(name,pre,las):
    sql=f"""
        update hust 
        set {name}='{las}'
        where {name}  REGEXP '.*{pre}.*'
    """
    try:
        cursor.execute(sql)
        db.commit()
        print("更新成功")
    except:
        db.rollback()
def Delete(id):
    sql=f"""
        delete from hust where hust_id={id}
    """
    try:
        cursor.execute(sql)
        db.commit()
        print("删除成功")
    except:
        db.rollback()

def askMysql():
    # 数据库包含序号，题目，作者，时间，分类，下载地址

    # 创建数据库中的表


    sql = """CREATE TABLE hust
    (
        hust_id bigint NOT NULL AUTO_INCREMENT,
        hust_title varchar(100) NULL,
        hust_author varCHAR(100) NULL,
        hust_date varCHAR(100) NULL,
        hust_subject varchar(100) NULL,
        hust_link varchar(100) NULL,
        primary key (hust_id)
    );"""
    cursor.execute("DROP TABLE IF EXISTS hust")
    cursor.execute(sql)
    print("成功创建表AI")
    # 插入数据
    for i in range(0, int(the_page)):
        Insert(i)
    # Select('hust_author','a')
    # Delete(1)
    # Update('hust_title','a','b')
if __name__ == "__main__":
    the_page = input("请问你想爬几篇论文：")
    # 调用函数读取数据
    getdata(baseurl + '&show=' + str(the_page))
    # 注意发现论文作者有的单词无法用’utf-8‘编码表示，所以要有errors="ignore"
    file = open('1.txt', mode='w', errors="ignore")
    for i in range(0, int(the_page)):
        file.write(str(i + 1) + ".")
        file.write(abstract_list[i] + "\n")
        file.write("date:" + date_list[i] + "\n")
        file.write("title:"+title_list[i] + "\n")
        file.write("authors:"+author_list[i] + '\n')
        file.write("subjects:" + subjects_list[i] + '\n\n')
    file.close()


    ok = input("是否要连接数据库[Y/N]")
    if ok == 'Y':
        askMysql()