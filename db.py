import pymongo
import requests
from bson.dbref import DBRef
from time import time
from datetime import  datetime


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
    us = get_name(user)
    if us:
        return us, COINS.find({'user': user}).count()
    else:
        if user:
            return None, None
        return "ewq", None


def add_transaction(from_user, to_user):
    coin = COINS.find_one({"user": from_user})
    print(coin)
    COINS.update({"string": coin["string"]}, {
            "string": coin["string"],
            "time": coin["time"],
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


# def get_transaction():
#     a = list(LOGS.find())
#     res = []
#     count = 0
#     for i in a:
#         print(i["coin"].as_doc().items())
#         if count <= 3:
#             res.append({"coin": i["coin"].as_doc().items()[1][1]["string"],
#                     "from": get_name(i["from"]),
#                     "to": get_name(i["to"]),
#                     "time": datetime.utcfromtimestamp(i["time"]).strftime('%Y-%m-%d %h:%M:s')})
#         else:
#             break
#         count += 1
#     return res



def group_money():
    agr = COINS.aggregate([{'$group': {'_id': '$user', 'total': {'$sum': 1}}},
                           {'$sort': {'total': -1}}])
    res = [(get_name(i["_id"]), i["total"]) for i in list(agr)]
    if len(res) > 10:
        res = res[:10]

    return res


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
            return None
    except:
        return