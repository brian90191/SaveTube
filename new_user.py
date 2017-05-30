from common.database import Database

Database.initialize()
Database.insert('user', {"account":"Terry", "email":"Mark@gmail.com", "password":"123456"})
data = Database.find_one('user', {"account":"Terry"})
print (data)

