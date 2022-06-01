from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_gender = db.Column(db.String(10), nullable=False)
    user_address = db.Column(db.String(255), nullable=True)
    user_number = db.Column(db.String(15), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    Peminjaman = db.relationship('Peminjaman', backref='user', lazy=True)

    def __init__(self, user_name, user_gender, user_address, user_number):
        self.user_name = user_name
        self.user_gender = user_gender
        self.user_address = user_address
        self.user_number = user_number


class Penulis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Penulis_name = db.Column(db.String(20), nullable=False)
    Penulis_gender = db.Column(db.String(10), nullable=False)
    Penulis_address = db.Column(db.String(255), nullable=True)
    Penulis_number = db.Column(db.String(15), nullable=True)
    Penulis_created = db.Column(db.DateTime, default=datetime.now)
    Buku = db.relationship('Buku', backref='penulis', lazy=True)

    def __init__(self, Penulis_name, Penulis_gender, Penulis_address, Penulis_number):
        self.Penulis_name = Penulis_name
        self.Penulis_gender = Penulis_gender
        self.Penulis_address = Penulis_address
        self.Penulis_number = Penulis_number


class Buku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'penulis.id'), nullable=False)
    buku_title = db.Column(db.String(100), nullable=False)
    Peminjaman = db.relationship('Peminjaman', backref='buku', lazy=True)

    def __init__(self, author_id, buku_title):
        self.author_id = author_id
        self.buku_title = buku_title


class Peminjaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buku_id = db.Column(db.Integer, db.ForeignKey('buku.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, buku_id):
        self.user_id = user_id
        self.buku_id = buku_id


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({
            'output': "ini get"
        }), 200
    else:
        return jsonify({
            'output': 'ini post'
        }), 201

# ============================================ AREA PENULIS ==============================================================


@app.route('/insert/penulis/', methods=['POST'])
def insertPenulis():
    new_input = request.get_json()
    Penulis_name = new_input['Penulis_name']
    Penulis_gender = new_input['Penulis_gender']
    Penulis_address = new_input['Penulis_address']
    Penulis_number = new_input['Penulis_number']
    new_penulis = Penulis(Penulis_name, Penulis_gender,
                          Penulis_address, Penulis_number)
    try:
        db.session.add(new_penulis)
        db.session.commit()
        return jsonify({
            'output': "Success"
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


@app.route('/get/penulis/', methods=["GET"])
def getPenulis():
    data_penulis = Penulis.query.order_by(Penulis.id).all()
    data_penulis_new = {}
    for penulis in data_penulis:
        data_penulis_new[penulis.id] = {
            'Penulis_name': penulis.Penulis_name,
            'Penulis_gender': penulis.Penulis_gender,
            'Penulis_address': penulis.Penulis_address,
            'Penulis_number': penulis.Penulis_number,
        }

    return jsonify({
        "output": data_penulis_new
    })


@app.route('/delete/penulis/', methods=["DELETE"])
def deletePenulis():
    new_input = request.get_json()
    id_penulis = new_input['id']
    delete_data = Penulis.query.get_or_404(id_penulis)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "User {} has been deleted".format(delete_data.Penulis_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


# Niatnya, pas mau update data, yang perlu dikirim cuman data yang pengen diubah aja, gak semua kolom
@app.route('/update/penulis/<int:id>', methods=["PUT"])
def updatePenulis(id):
    penulis = Penulis.query.get_or_404(id)
    update_data = request.get_json()
    for key, val in update_data.items():
        if key not in dir(penulis):
            return
        else:
            # epic sih ini, baru tau bisa kayak gini, biar flexible buat manggil nama method berdasarkan variable di val
            setattr(penulis, key, val)
            # setattr temennya getattr
    try:
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "User {} has been updated".format(penulis.Penulis_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })

# ============================================ Area Buku ==============================================================


@app.route('/insert/buku/', methods=['POST'])
def insertBuku():
    new_input = request.get_json()
    author_id = new_input['author_id']
    buku_title = new_input['buku_title']
    new_buku = Buku(author_id, buku_title)
    try:
        db.session.add(new_buku)
        db.session.commit()
        return jsonify({
            'output': "Success"
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


@app.route('/get/buku/', methods=["GET"])
def getBuku():
    data_buku = Buku.query.order_by(Buku.id).all()
    data_buku_new = {}
    for buku in data_buku:
        data_buku_new[buku.id] = {
            'author_id': buku.author_id,
            'buku_title': buku.buku_title
        }

    return jsonify({
        "output": data_buku_new
    })


@app.route('/update/buku/<int:id>', methods=["PUT"])
def updateBuku(id):
    buku = Buku.query.get_or_404(id)
    update_data = request.get_json()
    for key, val in update_data.items():
        if key not in dir(buku):
            return
        else:
            # epic sih ini, baru tau bisa kayak gini, biar flexible buat manggil nama method berdasarkan variable di val
            setattr(buku, key, val)
            # setattr temennya getattr
    try:
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "Book Data '{}' has been updated".format(buku.buku_title)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


@app.route('/delete/buku/', methods=["DELETE"])
def deleteBuku():
    new_input = request.get_json()
    id_buku = new_input['id']
    delete_data = Buku.query.get_or_404(id_buku)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "Book data '{}' has been deleted".format(delete_data.buku_title)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })

# ============================================ Area User ==============================================================


@app.route('/insert/user/', methods=['POST'])
def insertUser():
    new_input = request.get_json()
    user_name = new_input['user_name']
    user_gender = new_input['user_gender']
    user_address = new_input['user_address']
    user_number = new_input['user_number']
    new_user = User(user_name, user_gender,
                    user_address, user_number)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'output': "Success"
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


@app.route('/get/user/', methods=["GET"])
def getUser():
    data_user = User.query.order_by(User.id).all()
    data_user_new = {}
    for user in data_user:
        data_user_new[user.id] = {
            'user_name': user.user_name,
            'user_gender': user.user_gender,
            'user_address': user.user_address,
            'user_number': user.user_number,
        }
    print(data_user_new)
    return jsonify({
        "output": data_user_new
    })


@app.route('/delete/user/', methods=["DELETE"])
def deleteUser():
    new_input = request.get_json()
    id_user = new_input['id']
    delete_data = User.query.get_or_404(id_user)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "User {} has been deleted".format(delete_data.user_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


# Niatnya, pas mau update data, yang perlu dikirim cuman data yang pengen diubah aja, gak semua kolom
@app.route('/update/user/<int:id>', methods=["PUT"])
def updateUser(id):
    user = User.query.get_or_404(id)
    update_data = request.get_json()
    for key, val in update_data.items():
        if key not in dir(user):
            return
        else:
            # epic sih ini, baru tau bisa kayak gini, biar flexible buat manggil nama method berdasarkan variable di val
            setattr(user, key, val)
            # setattr temennya getattr
    try:
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "User '{}' has been updated".format(user.user_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })

# ============================================ Area Peminjaman ==============================================================


@app.route('/insert/peminjaman', methods=["POST"])
def insertPeminjaman():
    new_data = request.get_json()
    user_id = new_data['user_id']
    buku_id = new_data['buku_id']
    new_peminjaman = Peminjaman(user_id, buku_id)
    try:
        db.session.add(new_peminjaman)
        db.session.commit()
        return jsonify({
            'output': "Success"
        })
    except:
        return jsonify({
            'output': 'Failed'
        })


@app.route("/get/peminjaman", methods=["GET"])
def getPeminjaman():
    data_peminjaman = Peminjaman.query.order_by(Peminjaman.id).all()
    data_peminjaman_new = {}
    for peminjaman in data_peminjaman:
        data_peminjaman_new[peminjaman.id] = {
            'user_id': peminjaman.user_id,
            'buku_id': peminjaman.buku_id,
    }
    print(data_peminjaman_new)
    return jsonify({
        "output": data_peminjaman_new
    })

@app.route("/delete/peminjaman", methods=["DELETE"])
def deletePeminjaman():
    new_input = request.get_json()
    id_peminjaman = new_input['id']
    delete_data = Peminjaman.query.get_or_404(id_peminjaman)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments": "Peminjaman {} has been deleted".format(delete_data.id)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })

if __name__ == "__main__":
    app.run(debug=True)
