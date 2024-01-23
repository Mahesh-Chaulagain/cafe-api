import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    # Cafe TABLE Configuration
    class Cafe(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(250), unique=True, nullable=False)
        map_url = db.Column(db.String(500), nullable=False)
        img_url = db.Column(db.String(500), nullable=False)
        location = db.Column(db.String(250), nullable=False)
        seats = db.Column(db.String(250), nullable=False)
        has_toilet = db.Column(db.Boolean, nullable=False)
        has_wifi = db.Column(db.Boolean, nullable=False)
        has_sockets = db.Column(db.Boolean, nullable=False)
        can_take_calls = db.Column(db.Boolean, nullable=False)
        coffee_price = db.Column(db.String(250), nullable=True)

        def to_dict(self):
            # # Method 1
            # dictionary = {}
            # # loop through each column in the data record
            # for column in self.__table__.columns:
            #     # create a new dictionary entry where the key is the name of the column and
            #     # value is the value of the column
            #     dictionary[column.name] = getattr(self, column.name)
            # return dictionary

            # Method 2. Alternatively use Dictionary Compression to do the same thing
            return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    db.create_all()



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    # serialization: process of converting SQLAlchemy object into JSON
    # Jsonify: create a response with the JSON representation of the given arguments with an application/json mimetype

    # the method described below has maximum flexibility. It allows you to have perfect control over the JSON response
    # return jsonify(cafe={
    #     # "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #
    #     # put some properties in sub-category
    #     "amenities": {
    #         "seats": random_cafe.seats,
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "has_sockets": random_cafe.has_sockets,
    #         "can_take_calls": random_cafe.can_take_calls,
    #         "coffee_price": random_cafe.coffee_price,
    #     }
    # })
    # Another method of serializing our database row Object into JSON is by first converting it to a dictionary and
    # then use jsonify() to convert dictionary to a JSON
    return jsonify(cafe=random_cafe.to_dict())


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
