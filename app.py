import os
from flask import Flask, render_template, url_for, request, redirect, \
     flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Environment Variables
app.config["MONGO_DBNAME"] = "rehearsal_room"
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/the_band_room')
# Default landing page
def the_band_room():
    return render_template("addbandroom.html")


# This function adds a new band room
@app.route('/add_room', methods=['POST'])
def add_band_room():
    room_key = request.form["room_key"]
    # iterate over stored band rooms to check
    # if the name and room key are available
    check_key = mongo.db.band_rooms.count_documents((
        {"room_key": room_key}))
    if check_key > 0:
        # if name and room key are not available
        flash('Sorry that room key is unavailable', 'error')
        return redirect(url_for('the_band_room'))
    # if both name and key are available the room will be created
    else:
        new_room = mongo.db.band_rooms
        new_room.insert_one(request.form.to_dict())
        flash('Room created successfully', 'success')
        return redirect(url_for('browse_rooms'))


@app.route('/browse_rooms')
def browse_rooms():
    return render_template("browserooms.html",
                           band_rooms=mongo.db.band_rooms.find())


@app.route('/open_room')
def open_room():
    return render_template("openroom.html")


@app.route('/my_room', methods=['POST'])
def my_room():
    band_name = request.form["band_name_open"]
    room_key = request.form["room_key_open"]
    check_rooms = mongo.db.band_rooms.count_documents((
        {"room_key": room_key}))
    if check_rooms > 0:
        the_room = mongo.db.band_rooms.find_one(
            {"band_name": request.form["band_name_open"],
             "room_key": request.form["room_key_open"]})
        return render_template("bandroom.html",
                               the_room=the_room,
                               band_name=band_name,
                               room_key=room_key)
    else:
        flash('Oops seems like the Room Key was not right')
        return redirect(url_for('open_room'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'

    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
