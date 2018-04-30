from datetime import datetime

from flask import Flask
from flask import render_template, request
from hashlib import md5
import db


def check_hash(h):
    if "-" in h:
        user = h.split("-", maxsplit=1)[0]
        if db.is_new_string(h) and md5(h.encode('utf8')).hexdigest()[:5] == "00000":  # нашли хеш (здесь проверка для 4-х нулей)
            if not user.isdigit():
                return (False, None)
        else:
            return (False, None)
    else:
        return (False, None)
    return (True, user)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    res = []
    if request.method == "POST":
        hashes = request.form["hashes"].strip().split()
        for h in hashes:
            inf = check_hash(h)
            print(inf)
            error = not inf[0]
            user = inf[1]
            print(error)
            res.append((h, error))
            if not error:
                db.create_coin(user, h)
    return render_template('index.html', res=res)


@app.route('/wallet')
def wallet():
    user = request.args.get("ids", "")
    name, res = db.sumbit_coins(user)
    return render_template('wallet.html', res=res, name=name)


@app.route('/send', methods=['GET', 'POST'])
def send():
    res = " "
    tr = ""
    if request.method == "POST":
        user_from = request.form["ids_from"].strip()
        user_to = request.form["ids_to"].strip()
        count = request.form["count"].strip()
        print( db.get_name(user_from))
        try:
            if not db.get_name(user_from) or not db.get_name(user_to):
                res = "Такого пользователя нет"
            elif user_to == user_from:
                res = "Вы пытаетесь перевести деньги самому себе"
            elif not db.sumbit_coins(user_from)[1] >= int(count) and int(count) > 0:
                res = "Недостаточно монет"
            else:
                res = 0
                for i in range(int(count)):
                    db.add_transaction(user_from, user_to)
                tr = {"from": db.get_name(user_from), "to": db.get_name(user_to), "count": count,
                  "time": str(datetime.utcnow())}
        except Exception as e:
            print(e)
            res = "Укажите кол-во монет"


    return render_template('send.html', res=res, tr = tr)


@app.route('/top')
def top():
    res = db.group_money()
    return render_template('top.html', res=res)


if __name__ == "__main__":
    app.run(port=8080, host = "localhost")


# 2-rf0jn3x9nctmkx5su4wfxwdq11zbewtxna1pubncz12mi0ul
# 9857-cecksdjkdsfjdsf
# 9857-cecksdjkdsfjdsf
# 5-cksdjkds
# 4gr-dddv
# 45686-ghhffgb
