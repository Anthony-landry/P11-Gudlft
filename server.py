#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation du flask : micro framework open-source de développement web en Python.
from flask import Flask, render_template, request, redirect, flash, url_for

import utils
# import les fonctions du fichiers utils
from utils import *

app = Flask(__name__)
app.secret_key = 'something_special'


# Fonction qui retourne la page de connexion.
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


# Fonction qui permet de demander la réservation de place.
@app.route('/book/<competition>/<club>', methods=['POST', 'GET'])
def book(competition, club):
    """
    Il faut faire attention à ne pas melanger competition ici,
    qui contient le nom de la compétition et l'object
    competition issus du JSON sous forme de dictionnaire
    """

    # Vérification du club.
    if not clubExist(club):
        flash("Club doesn't exist")
        return render_template('index.html'), 404

    # Vérification de la competition.
    if not competitionExist(competition):
        flash("Competions doesn't exist")
        return render_template('welcome.html'), 404

    # Vérification de la date de la competition.
    error_page = verifyCompetitionPlaces(getCompet(competition), getClub(club), 'welcome.html')
    if error_page:
        return error_page

    return render_template('booking.html', club=getClub(club), competition=getCompet(competition))


# Fonction qui permet de reserver la réservation de place.
@app.route('/purchasePlaces', methods=['POST', 'GET'])
def purchasePlaces():
    # Pas de club trouvé.
    error_page = checkClubData()
    if error_page:
        return error_page
    else:
        club_name = request.form['club']

    # vérification si le club existe.
    if not clubExist(club_name):
        flash("Unkown club.", 'error')
        return render_template('index.html'), 401
    else:
        club = getClub(club_name)

    # Pas de compétition trouvé.
    error_page = checkCompetitionData(club)
    if error_page:
        return error_page
    else:
        competition_name = request.form['competition']

    # Vérifie que la competition existe.
    if not competitionExist(competition_name):
        flash("Competition doesn't exist")
        return render_template('welcome.html', club=club, competitions=loadCompetitions()), 404
    else:
        competition = getCompet(competition_name)

    # Pas de places trouvés.
    error_page = checkPlacesData(club, competition)
    if error_page:
        return error_page
    else:
        places = request.form['places']

    # Nombre de places invalide 'type, value'  doit etre entre 1 - 12 --> 401/412.
    error_page = verifyPlaces(request.form['places'], club, competition)
    if error_page:
        return error_page
    else:
        placesRequired = int(request.form['places'])

    # Vérification que l'on peut reserver la competition (non terminée).
    error_page = verifyCompetitionPlaces(competition, club, "booking.html")  # --> 410
    if error_page:
        return error_page

    error_page = verifyClubPlaces(placesRequired, club, competition)
    if error_page:
        return error_page

    # Mise à jour de la variable globale.
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    majCompet(competition)

    # Mise à jour de la variable globale.
    club['points'] = str(int(club['points']) - placesRequired)
    majClub(club)

    flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=loadCompetitions())


# Fonction qui montre un résumé de tous les clubs.
@app.route("/displayPoints", methods=['GET'])
def displayPoints():
    return render_template('displayPoints.html', clubs=loadClubs())


# Fonction pour se déconnecter du programme.
@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
#   for developing
   app.run(debug=True)
