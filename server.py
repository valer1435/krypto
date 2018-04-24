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
                user, stroka = h.split("-", maxsplit=1)
                if db.is_new_string(stroka) and md5(stroka.encode('utf8')).hexdigest()[:len(user)] == user:  # нашли хеш (здесь проверка для 4-х нулей)
                    if not user.isdigit():
                        error = True
                else:
                    error = True
            else:
                error = True
            res.append((h, error))
            if not error:
                db.create_coin(user, stroka)

    return render_template('index.html', res=res)

if __name__ == "__main__":
    app.run(port=8080, host = "localhost")


# 2-rf0jn3x9nctmkx5su4wfxwdq11zbewtxna1pubncz12mi0ul
# 9857-cecksdjkdsfjdsf
# 9857-cecksdjkdsfjdsf
# 5-cksdjkds
# 4gr-dddv
# 45686-ghhffgb
