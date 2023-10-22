#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation de la librairie json.
import json
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
		
		
# Variables globales.
competitions = loadCompetitions()
clubs = loadClubs()


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
	
# ------ DATA JSON BDD MANIPULATION ------
# CLUBS -------------------------------
# Fonction qui prend une liste de club en parametre et la converti en dictionnaire indices par email.
def getClubsToDictEmail(list_clubs):
    global competitions, clubs
    clubs_by_email = {club['email']: club for club in list_clubs}  # Les compréhensions de dictionnaire
    return clubs_by_email