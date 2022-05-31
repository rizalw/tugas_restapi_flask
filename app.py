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

    def __init__(self, author_id, buku_title):
        self.author_id = author_id
        self.buku_title = buku_title

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


@app.route('/delete/penulis/', methods=["POST"])
def deletePenulis():
    new_input = request.get_json()
    id_penulis = new_input['id']
    delete_data = Penulis.query.get_or_404(id_penulis)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return jsonify({
            'output': "Success",
            "comments" : "User {} has been deleted".format(delete_data.Penulis_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })

# Niatnya, pas mau update data, yang perlu dikirim cuman data yang pengen diubah aja, gak semua kolom
@app.route('/update/penulis/<int:id>', methods = ["POST"])
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
            "comments" : "User {} has been updated".format(penulis.Penulis_name)
        })
    except:
        return jsonify({
            'output': 'Failed'
        })    

# ============================================ Area Buku ==============================================================
@app.route('/insert/buku/', methods = ['POST'])
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

if __name__ == "__main__":
    app.run(debug=True)
