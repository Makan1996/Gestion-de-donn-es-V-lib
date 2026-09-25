import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["velib_rennes_vinci"]
mycol = mydb["velibCol"]

# x = mycol.find_one()
#
# print(x)
print("*************************************************")


for x in mycol.find():#he find() method returns all occurrences in the selection
  print(x)