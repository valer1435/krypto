from flask import Flask
from flask import render_template, request
from hashlib import md5

import db


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    res = []
    if request.method == "POST":
        hashes = request.form["hashes"].strip().split()
        for h in hashes:
            error = False
            if "-" in h:
                user= h.split("-", maxsplit=1)[0]
                if db.is_new_string(h) and md5(h.encode('utf8')).hexdigest()[:5] == "00000":  # нашли хеш (здесь проверка для 4-х нулей)
                    if not user.isdigit():
                        error = True
                else:
                    error = True
            else:
                error = True
            res.append((h, error))
            if not error:
                db.create_coin(user, h)
    return render_template('index.html', res=res)


@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    res = ""
    if request.method == "POST":
        user = request.form["ids"].strip()
        print(user)
        res = db.sumbit_coins(user)
    return render_template('wallet.html', res=res)


@app.route('/send', methods=['GET', 'POST'])
def send():
    res = 2
    if request.method == "POST":
        user_from = request.form["ids_from"].strip()
        user_to = request.form["ids_to"].strip()
        count = request.form["count"].strip()
        try:

            if not user_from.isdigit() or not user_to.isdigit() or not (db.sumbit_coins(user_from) >= int(count) and int(count) > 0):
                res = 0
            else:
                res = 1
        except:
            res = 0
        if res:
            for i in range(int(count)):
                db.add_transaction(user_from, user_to)
    return render_template('send.html', res=res)


@app.route('/top', methods=['GET'])
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
