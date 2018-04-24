import pymongo
import requests
from bson.dbref import DBRef
from time import time


#mongod --dbpath E:\PythonProjects\krypta\data\db

client = pymongo.MongoClient("localhost", 27017)
COINS = client.maindb.coin
LOGS = client.maindb.log
print(client.server_info())
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


def sumbit_coins(user):
    return COINS.find({'user': user}).count()


def add_transaction(from_user, to_user):
    coin = COINS.find_one({"user": from_user})
    COINS.update({"string": coin["string"]}, {
            "string": "$string",
            "time": "$time",
            "user": to_user,
        })

    LOGS.insert_one(
        {
            "coin": DBRef('coins', coin),
            "from": from_user,
            "to": to_user,
            "time": time()
        }
    )


def group_money():
    agr = COINS.aggregate([{'$group': {'_id': '$user', 'total': {'$sum': 1}}},
                           {'$sort': {'total': -1}}])
    return [(get_name(i["_id"]), i["total"]) for i in list(agr)]


def get_name(id):
    try:
        response = requests.get("https://api.vk.com/method/users.get", params={
            "user_ids": id,
            "version" : "5.72"
        })
        if response:
            resp_json = response.json()["response"]
            print(resp_json[0])
            return resp_json[0]["first_name"]+" "+resp_json[0]["last_name"]
        else:
            return "NULL"
    except:
        return "NULL"