#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from server import app

"""
BUG: Booking places in past competitions

"""


class BookTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):  # before testing
        pass

    # CAS NOMINAUX
    # - reservation pour une competition future (> aujourd'hui) avec club["points"] > 1

    def test_validBook_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 200)

    def test_validBook_data(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertIn(competition, result.data.decode())  # page booking

    # CAS LIMITES
    # - date == aujourd'hui (la competition n'a pas commencée)

    def test_limite_Date_Book_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Book_TestUnitaire_limit"
        club = "Book_Test_club"

        print("ERROR : change date to today in Book_TestUnitaire_limit")
        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 200)

    def test_limite_Date_Book_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Book_TestUnitaire_limit"
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertIn(competition, result.data.decode())  # page booking

    # - reservation pour une competition future (> aujourd'hui) avec club["points"] = 1

    def test_limite_club_point_Book_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Book_Test_club_limit"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 200)

    def test_limite_club_point_Book_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Book_Test_club_limit"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertIn(competition, result.data.decode())  # page booking

    # CAS ERREURS
    # - la competition n'existe pas
    def test_competition_pas_validBook_HTTPcode(self):  # TEST ERREUR --> ça ne doit pas marcher
        competition = ""
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 404)

    # on ne teste pas le contenu car cela renvoie une erreur et donc pas de page

    # - le club n'existe pas

    def test_club_pas_validBook_HTTPcode(self):  # TEST ERREUR--> ça ne doit pas marcher
        competition = "Book_TestUnitaire_open"
        club = ""

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 404)

    # - reservation de place pour un concours qui est complet (numberOfPlaces = 0)
    def test_competition_complet_validBook_HTTPcode(self):  # TEST ERREUR--> ça ne doit pas marcher
        competition = "Book_TestUnitaire_open_full"
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 410)

    # - competition est finie
    def test_competition_finie_validBook_HTTPcode(self):  # TEST ERREUR--> ça ne doit pas marcher
        competition = "Book_TestUnitaire_closed"
        club = "Book_Test_club"

        result = self.client.post("/book/" + competition + "/" + club)
        self.assertEqual(result.status_code, 410)

    #
    def tearDown(self):  # after testing
        pass

    """
    410 : Gone
    This response is sent when the requested content has been permanently deleted from server, 
    with no forwarding address. Clients are expected to remove their caches and links to the resource. 
    The HTTP specification intends this status code to be used for "limited-time, promotional services". 
    APIs should not feel compelled to indicate resources that have been deleted with this status code.
    """
