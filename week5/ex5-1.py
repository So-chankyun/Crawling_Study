import pymysql
from openpyxl import workbook
from openpyxl import load_workbook

class MysqlController:
    def __init__(self, host, id, pw, db_name):
        self.conn = pymysql.connect(host=host, user=id,password=pw,db=db_name)
        self.curs = self.conn.cursor()

    def select_all(self):
        try:
            with self.curs as cur:
                sql = "select * from fruits"
                cur.execute(sql)
                rs = cur.fetchall()
                for row in rs:
                    print(row)
        except:
            print('error')

    def read_image(self):
        try:
            with open("./fruits/apple.jpg",'rb') as f: # 왜 파일이 안읽히는지 모르겠음.
                img = f.read()
                print(img)
        except:
            print('read error')
        finally:
            return img
    
    def insert_data_to_db(self):
        try:
            data = self.read_image()
            print('read data')
            sql = 'insert into fruits(name,image) values (%s,)'
            self.curs.execute(sql,('apple',data))
            self.conn.commit()
        except:
            print('insert error')

if __name__ == "__main__":
    db = MysqlController('localhost','root','skdltm97','test')
    db.insert_data_to_db()
    db.select_all()

