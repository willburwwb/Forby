import pymysql
class MYSQL(object):
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", port=3308, user="root", password="wwb20030526", db="test")
        self.cursor = self.conn.cursor()
    def Select(self,name,ask_name):
        sql = f"""
                select {name},hust_link from hust
                where {name} REGEXP '.*{ask_name}.*'
           """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def Delecet(self,name,ask_name):
        sql = f"""
                delete from hust 
                where {name} REGEXP '.*{ask_name}.*'
            """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
             self.conn.rollback()
             return 0
        else:
             return 1
    def Updata(self,name,ask_name,las_name):
        sql = f"""
                update hust
                set {name}='{las_name}' 
                where {name} REGEXP '.*{ask_name}.*'
            """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
             self.conn.rollback()
             return 0
        else:
             return 1
    def close(self):
        self.conn.close()
        self.cursor.close()
