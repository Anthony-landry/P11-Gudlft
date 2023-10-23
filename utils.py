#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation de la librairie json.
import json
# Import de la librairie datetime : pour la gestion des dates.
import datetime
# Importation du flask : micro framework open-source de développement web en Python.
from flask import request, flash, render_template


# Import des constantes du module const.
from const import *

# ------ INPUT / OUTPUT ------
# Fonction qui charge les données des clubs du fichier JSON.
def loadClubs():
    with open(FILE_CLUB, "r") as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs
		
# Fonction qui charge les données des compétitions du fichier JSON.
def loadCompetitions():
    with open(FILE_COMPETITION, "r") as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions
		
# Fonction qui sauvegarde les données des compétitions dans le fichier JSON.
def saveClubs(saved_club):
    with open(FILE_CLUB_SAVE, "w") as c:
        json.dump({"clubs": saved_club}, c, indent=4)


# Fonction qui sauvegarde les données des compétitions dans le fichier JSON.
def saveCompetitions(saved_competitions):
    with open(FILE_COMPETITION_SAVE, "w") as c:
        json.dump({"competitions": saved_competitions}, c, indent=4)
		
		
# Variables globales.
competitions = loadCompetitions()
clubs = loadClubs()

# ------ DATE ------
def get_time_now():
    return datetime.datetime.now()


def dateString_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


# Fonction qui charge les données des compétitions du fichier JSON.
def loadCompetitions():
    with open(FILE_COMPETITION, "r") as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions
		
		
#  ------ DATA HTML FORM ------
# Fonction qui verifie que l'email est présent dans la requete venant de la page .
def checkEmailData():
    if 'email' not in request.form:
        flash("No email.", 'error')
        return render_template('index.html'), 401

    # Vérification que le mail n'est pas vide.
    if len(request.form['email']) == 0:
        flash("Empty email.", 'error')
        return render_template('index.html'), 401
    return None
	
# Fonction qui verifie que le club est présent dans la requete venant de la page .
def checkClubData():
    if 'club' not in request.form:
        flash("Empty club.", 'error')
        return render_template('index.html'), 404
    return None
	
# Fonction qui verifie que la competition est présent dans la requete venant de la page.
def checkCompetitionData(club):
    if 'competition' not in request.form:
        flash("No competition.", 'error')
        return render_template('welcome.html', club=club, competitions=competitions), 404
    return None
	
# Fonction qui verifie que le nombre de places est présent dans la requete venant de la page.
def checkPlacesData(club, competition):
    if 'places' not in request.form:
        flash("No places.", 'error')
        return render_template('booking.html', club=club, competition=competition), 401
    return None
	
# ------ DATA JSON BDD MANIPULATION ------
# CLUBS -------------------------------
	
# Fonction qui retourne le club correspondant au parametre nom.
def getClub(name):
    global competitions, clubs
    for name_club, club in getClubsToDictName(clubs).items():
        if name_club == name:
            return dict(club)  # on recrée un dictionnaire pour eviter le pointeur
			
# Fonction qui converti la listre des compétitions en dictionnaire.
def getCompetitionsToDictName(list_competitions):
    global competitions, clubs
    
    competitions_by_name = {compet['name']: compet for compet in
                            list_competitions}  # Les compréhensions de dictionnaire
    return competitions_by_name
			
# Fonction qui retourne la compétition en fonction de son nom.
def getCompet(name):
    global competitions, clubs
    
    for name_compet, compet in getCompetitionsToDictName(competitions).items():
        if name_compet == name:
            return dict(compet)  # on recrée un dictionnaire pour eviter le pointeur
	
# ------ DATA JSON BDD MANIPULATION ------
# CLUBS -------------------------------
# Fonction qui prend une liste de club en parametre et la converti en dictionnaire indices par email.
def getClubsToDictEmail(list_clubs):
    global competitions, clubs
    clubs_by_email = {club['email']: club for club in list_clubs}  # Les compréhensions de dictionnaire
    return clubs_by_email
	
# Fonction qui prend une liste de club en parametre et la converti en dictionnaire indices par nom.
def getClubsToDictName(list_clubs):
    global competitions, clubs
    clubs_by_name = {club['name']: club for club in list_clubs}  # Les compréhensions de dictionnaire
    return clubs_by_name
	
# Fonction qui retourne si le club existe
def clubExist(club):
    global competitions, clubs
    return club in [c["name"] for c in clubs]
	
# COMPETITIONS -------------------------------
# Fonction qui vérifie que la compétition existe.
def competitionExist(competition_name):
    global competitions, clubs

    return competition_name in [c["name"] for c in competitions]
	
# Fonction qui vérifie que la compétition est finie.
def competitionIsFinished(competition):
    global competitions, clubs
    
    assert competitionExist(competition["name"]), "competition doesn't exist"
    return get_time_now() > dateString_to_date(competition["date"])
	
# Fonction qui vérifie que la compétition a des places disponibles.
def competitionHasPlace(competition):
    global competitions, clubs
    
    assert competitionExist(competition["name"]), "competition doesn't exist"
    return int(competition['numberOfPlaces']) > 0
	
# Fonction qui vérifie que le client peux reserver des places dans une compétition.
def verifyCompetitionPlaces(competition, club, page):
    """
        Fonction qui vérifie que le client peux reserver des places dans une compétition.
    :param competition: la competition que l'on veut reserver
    :type competition: dict
    :param club: le club qui veut reserver
    :type club: dict
    :param page: le nom de la page html qui faut retourner
    :type page: str
    :return: la page html si erreur , None sinon
    :rtype: str, None
    """
    global competitions, clubs
    
    assert competition in competitions

    error = False
    # on vérifie que l'on peut reserver la competition (non terminée)
    if competitionIsFinished(competition):
        flash("Competition is finished")
        error = True

    if not competitionHasPlace(competition):
        flash("Competition is complete")
        error = True

    if error:
        if "welcome" in page:
            return render_template(page, club=club, competitions=competitions), 410
        else:
            return render_template(page, club=club, competition=competition), 410

    return None
	
# PLACES -------------------------------
# Fonction qui vérifie si le nombre de place demandé par le club est correct.
def verifyPlaces(places, club, competition):
    """
    Fonction qui vérifie si le nombre de place demandé par le club est correct.

    :param places: place que veut réserver le club
    :type places: str
    :param club: Nom du club
    :type club: str
    :param competition: nom de la compétition
    :type competition: str
    :return: la page html si erreur , None
    :rtype str, None
    """
    global competitions, clubs
    
    try:
        if int(places) <= 0 or int(places) > 12:
            flash("Number of place isn't valid {1, ..., 12}", 'error')
            return render_template('booking.html', club=club, competition=competition), 401
    except ValueError:
        flash("TypeError number of place", 'error')
        return render_template('booking.html', club=club, competition=competition), 401

    return None


# Fonction qui vérifie si le nombre de place ets disponible pour le club la compétrition .
def verifyClubPlaces(places, club, competition):
    """

    :param places: place que veut réserver le club
    :type places: int
    :param club: Nom du club
    :type club: str
    :param competition: nom de la compétition
    :type competition: str
    :return: la page html si erreur ,

    """
    global competitions, clubs
    
    placesRequired = int(places)

    # on verifie que le nombre de place demandées est plus petit ou egal aux nombres de places disponible.
    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Competition has not enough places")
        return render_template('welcome.html', club=club, competitions=competitions), 412

    # on verifie que le nombre de points du club est supérieur au nombre de places demandées.
    if placesRequired > int(club["points"]):

        flash("number of point isn't enough")
        return render_template('welcome.html', club=club, competitions=competitions), 412
	
	
# -------- MAJ DES POINTS
# Fonction qui met à jour les points du club.
def majClub(club):
    global competitions, clubs

    clubs = [cl if cl["name"] != club["name"] else club for cl in clubs]
    
    saveClubs(clubs)
    
    clubs = loadClubs()


# Fonction qui met à jour les points de la competition.
def majCompet(compet):
    global competitions, clubs

    competitions = [c if c["name"] != compet["name"] else compet for c in competitions]
    
    saveCompetitions(competitions)
    
    competitions = loadCompetitions()