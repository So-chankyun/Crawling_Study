import sqlite3

con = sqlite3.connect('C:/Users/chank/Python38-32/크롤링 자료/study/example.db') # 데이터베이스 파일 생성
cur = con.cursor()
# 테이블 정의
# SQL = 'CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)'
# cursor.execute(SQL)

# tuple 삽입
# cursor.execute("INSERT INTO kakao VALUES('16.06.03',97000,98000,96900,98000,321405)")
# cursor.execute("INSERT INTO kakao VALUES('16.06.02',99000,99300,96300,97500,556990)")

# con.commit()

# table 조회
cur.execute("SELECT * FROM kakao")
for row in cur:
    print(row)

con.close()
