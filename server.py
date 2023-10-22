import json
from flask import Flask, render_template, request, redirect, flash, url_for

import utils
# import les fonctions du fichiers utils
from utils import *


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    return render_template('index.html')


# Fonction qui donne les informaitons du club.
@app.route('/showSummary', methods=['POST', 'GET'])
def showSummary():
    # Vérification que l'on recoit bien le champ 'email' --> COTE FRONT END.
    error_page = checkEmailData()
    if error_page:
        return error_page

    # Vérification que notre mail existe dans la base --> COTE BACK END (validité).
    clubs_by_email = getClubsToDictEmail(loadClubs())
    if request.form["email"] not in clubs_by_email.keys():
        flash("Email not valid.", 'error')
        return render_template('index.html'), 403
    else:
        club = clubs_by_email[request.form["email"]]

        return render_template(
            'welcome.html',
            club=club,
            competitions=loadCompetitions()
        )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    #   for developing
    app.run(debug=True)
