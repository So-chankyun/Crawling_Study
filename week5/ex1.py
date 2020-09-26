from tinydb import Query, TinyDB

filename = "test2.json"
db = TinyDB(filename)
db.drop_table('fruits')
table = db.table('fruits') # 테이블 생성

# tuple 삽입
table.insert({'name':'사과','price':5000})
table.insert({'name':'바나나','price':7000})
table.insert({'name':'망고','price':8000})
table.insert({'name':'레몬','price':5500})

# tuple 조회
print(table.all())

item = Query()
# 특정 조건의 tuple을 검색
res = table.search(item.name == '사과')
print(res[0]['name']) # 반환은 리스트 형태라서 res[0]를 붙임

res = table.search(item.price > 6000)

for i in res:
    print('-',i['name'],i['price'])