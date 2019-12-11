import os
import sqlite3

from flask import Flask, url_for, flash
from flask import render_template
from flask import request, redirect
from flask import g
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from operator import itemgetter
from collections import defaultdict

project_dir = os.path.abspath(os.path.dirname(__file__))
database_file = "sqlite:////" + (os.path.join(project_dir, "flowers2019.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

engine = create_engine(database_file)

# DISPLAY ALL FLOWERS
@app.route("/", methods=["GET", "POST"])
def getFlowers():
    connection = engine.connect()
    flowers = connection.execute("SELECT * FROM FLOWERS")
    return render_template('home.html', flowers=flowers)
    connection.close()

### RETURN RECENT SIGHTINGS
@app.route("/sightings/<string:name>", methods=["GET", "POST"])
def getSightings(name):
    connection = engine.connect()
    sighting = connection.execute("SELECT * FROM SIGHTINGS WHERE NAME = :NAME",{"NAME":name}).fetchall()

    myList = []
    myList = sighting

    count = 0
    newList = []
    for row in sighting:
        dateStr = myList[count][3]
        date = dateStr.replace("-","")
        intDate = int(date)
        newList.append((myList[count][0], myList[count][1], myList[count][2], intDate))
        count = count + 1

    sortedList = sorted(newList, reverse = True, key=lambda x: int(x[3]))[:10]

    listCnt = 0
    finalList = []
    for row in sortedList:
        dateNum = sortedList[listCnt][3]
        date = str(dateNum)
        dateStr = '-'.join(date[i:i+2] for i in range(0, len(date), 2))
        finalStr = dateStr.replace('-', '', 1)
        finalList.append((sortedList[listCnt][0], sortedList[listCnt][1], sortedList[listCnt][2], finalStr))
        listCnt = listCnt + 1

    return render_template('sightings.html', sighting=finalList)
    connection.close()


### ADD FLOWER TO DB
@app.route("/new/", methods=["GET", "POST"])
def add():
    connection = engine.connect()
    newComname = request.args.get('comname')
    newGenus = request.args.get('genus')
    newSpecies = request.args.get('species')
    newComnameStr = str(newComname)
    newGenusStr = str(newGenus)
    newSpeciesStr = str(newSpecies)
    connection.execute("""INSERT INTO flowers(genus, species, comname) VALUES(:genus, :species, :comname)""",
    {"genus":newGenusStr, "species":newSpeciesStr, "comname":newComnameStr})
    flowers = connection.execute("SELECT * FROM FLOWERS")
    return redirect(url_for('getFlowers'))
    connection.close()


### DELETE FLOWER FROM FLOWERS DB (not sure if we need to delete from sightings too)
@app.route("/delete/<string:comname>", methods=["POST"])
def delete(comname):
    connection = engine.connect()
    connection.execute("""DELETE FROM FLOWERS WHERE comname = :comname""",{"comname":comname})
    flowers = connection.execute("SELECT * FROM FLOWERS")
    return redirect(url_for('getFlowers'))
    connection.close()


### ADD NEW SIGHTING
@app.route("/newSighting/", methods=["GET", "POST"])
def newSighting():
    connection = engine.connect()
    newName = request.args.get('name')
    newPerson = request.args.get('person')
    newLocation = request.args.get('location')
    newSighted = request.args.get('sighted')
    nameStr = str(newName)
    personStr = str(newPerson)
    locationStr = str(newLocation)
    sightedStr = str(newSighted)
    connection.execute("""INSERT INTO SIGHTINGS(name, person, location, sighted) VALUES(:name, :person, :location, :sighted)""",
    {"name":nameStr, "person":personStr, "location":locationStr, "sighted":sightedStr})
    return redirect(url_for('getFlowers'))
    connection.close()


# ## EDIT FLOWER PAGE RENDER
@app.route("/on_edit/", methods=["GET", "POST"])
def on_edit():
    return render_template('edit.html')


### EDIT FLOWER
@app.route("/edit/", methods=["GET", "POST"])
def edit():
    connection = engine.connect()
    comname = request.args.get('comname')
    newGenus = request.args.get('genus')
    newSpecies = request.args.get('species')
    comnameStr = str(comname)
    newGenusStr = str(newGenus)
    newSpeciesStr = str(newSpecies)
    updateRow = connection.execute("UPDATE FLOWERS SET genus=:genus WHERE comname=:comname",
    {"comname":comnameStr, "genus":newGenusStr})
    updateRow = connection.execute("UPDATE FLOWERS SET species=:species WHERE comname=:comname",
    {"comname":comnameStr, "species":newSpeciesStr})
    return redirect(url_for('getFlowers'))
    connection.close()

if __name__ == "__main__":
    app.run(debug=True)
