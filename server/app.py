#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries]), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_data = bakery.to_dict()
        bakery_data['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
        return jsonify(bakery_data), 200
    return make_response({'error': 'Bakery not found'}, 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([bg.to_dict() for bg in baked_goods]), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict()), 200
    return make_response({'error': 'No baked goods found'}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
