from flask import Flask, redirect, url_for, request,render_template
from User_mysql import MYSQL
from getdata import myData
import pymysql
app = Flask(__name__)

@app.route('/')
def login():
   return render_template("login.html")

@app.route('/index/')
def index():
   return render_template("index.html")

@app.route('/ans',methods=['GET',"POST"])
def answer():
   name = request.form.get('name')
   ask_name = request.form.get('ask_name')
   db = MYSQL()
   results = db.Select(name, ask_name)
   db.close()
   return render_template("success.html",name=name,results=results)
@app.route('/other',methods=['GET',"POST"])
def other():
   del_name = request.form.get('del_name')
   del_ask_name = request.form.get('del_ask_name')
   upd_name=request.form.get('upd_name')
   upd_ask_name = request.form.get('upd_ask_name')
   las_ask_name = request.form.get('las_ask_name')
   db = MYSQL()
   if del_name!=None :
      results = db.Delecet(del_name, del_ask_name)
   else:
      results = db.Updata(upd_name,upd_ask_name,las_ask_name)
   db.close()
   return render_template('other.html',results=results)

@app.route('/getdata/',methods=['GET',"POST"])
def mydata():
   baseurl = "https://arxiv.org/list/cs.AI/pastweek?skip=0"
   the_page = request.form.get('name')
   print(the_page)
   page=int(the_page)
   OneData = myData(the_page)
   OneData.getdata(baseurl + '&show=' + str(the_page))
   OneData.askMysql()
   return "YES"


if __name__ == '__main__':
   app.run(host='127.0.0.1')