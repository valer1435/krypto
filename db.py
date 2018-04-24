import pymongo
from bson.dbref import DBRef
from time import time


#mongod --dbpath E:\PythonProjects\krypta\data\db

client = pymongo.MongoClient("localhost", 27017)
COINS = client.maindb.coin
LOGS = client.maindb.log


def create_coin(user, stroka):
    COINS.insert_one(
        {
            "string": stroka,
            "time": time(),
            "user": user,
        }
    )
    print(stroka)


def is_new_string(string):
    if list(COINS.find({'string': string})):
        return False
    return True


# print(client.maindb.log.find_one()["coin"].collection)
#
# client.maindb.coins.create_index("user")