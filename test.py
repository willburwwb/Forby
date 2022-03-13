from urllib import request
from bs4 import BeautifulSoup
# 查询网址，将html文件搞下来

def askurl(url):
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"
    }
    req=request.Request(url=url,headers=headers)
    res=request.urlopen(req)
    return res.read().decode("utf-8")


author_list = []
title_list = []
abstract_list = []
subjects_list = []
date_list = []
rest_date = 0
def getdata(url):
    bs = BeautifulSoup(askurl(url), "html.parser")
    # data = bs.select('div #dlpage>h3')
    # print("今日时间："+data[0].text[0:16])
    title = bs.select("div#dlpage > dl > dd > div > div.list-title.mathjax")
    author = bs.select("dd > div.meta > div.list-authors")
    abstract = bs.select('div#dlpage> dl > dt > span >a[title="Abstract"]')
    subjects = bs.select("dd > div.meta > div.list-subjects > span.primary-subject")
    for i in range(0, 25):
        # if rest_date == 0:
        #     date = bs.select('div #dlpage>h3')
        #     date_list.append(date[0].text[0:16]+'\n')
        # else:
        #     rest_date = rest_date-1
        title_list.append(title[i].text)
        author_list.append(author[i].text)
        author_list[i] = author_list[i].replace('\n','')
        abstract_list.append(abstract[i].text)
        subjects_list.append(subjects[i].text)
firurl = "https://arxiv.org/list/cs.AI/recent"
baseurl = "https://arxiv.org/list/cs.AI/pastweek?skip="
if __name__ == "__main__":
    the_page=input("请问你想爬几页：")
    for page in range(0, int(the_page)):
        if page == 0:
            getdata(firurl)
        else:
            getdata(baseurl+str(page*25)+'&show25')

    file = open('1.txt', mode='w')
    for i in range(0, 25*int(the_page)-1):
        file.write(abstract_list[i])
        file.write(title_list[i])
        #file.write(author_list[i]+'\n')
        file.write("subjects:"+subjects_list[i]+'\n\n')
    file.close()


