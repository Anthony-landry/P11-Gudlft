#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from server import app


"""
BUG: Clubs shouldn't be able to book more than 12 places per competition

BUG: Clubs should not be able to use more than their points allowed
"""


class PurchasePlacesTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):  # before testing
        pass

    # CAS NOMINAUX
    # - reservation d' 1 place pour une competition future (> aujourd'hui) avec club["points"] > 1
    def test_valide_Purchase_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Purchase_Test_club"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_valide_Purchase_data(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Purchase_Test_club"
        club_email = "test_club@email.com"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - reservation de n (n < 12 && nb < club["points"] && nb < competitions["numberOfPlaces"] pour une competition
    # future (> aujourd'hui) avec un nb de points suffisant

    def test_valide_Purchase_n_place_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Purchase_Test_club"
        places = 7

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_valide_Purchase_n_place_data(self):  # TEST NOMINAL --> ça doit marcher

        competition = "Book_TestUnitaire_open"
        club = "Purchase_Test_club"
        club_email = "test_club@email.com"
        places = 7

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # CAS LIMITES
    # - reservation de 12 places sur 12 places disponibles

    def test_limite_12_12_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_12_1"
        club = "Purchase_Test_club_12_1"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_12_12_Purchase_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_12_2"
        club = "Purchase_Test_club_12_2"
        club_email = "test_club@email.com"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - reservation de 12 places sur +12 places disponibles

    def test_limite_12_12_plus_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_12_3"
        club = "Purchase_Test_club_12_3"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_12_12_plus_Purchase_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_12_4"
        club = "Purchase_Test_club_12_4"
        club_email = "test_club@email.com"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - reservation de n (n<12) places sur n places disponibles

    def test_limite_n_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_n"
        club = "Purchase_Test_club_n"
        places = 8

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_n_Purchase_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_n2"
        club = "Purchase_Test_club_n2"
        club_email = "test_club@email.com"
        places = 8

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - reservation de 12 places et club["points"] = 12 et competitions["numberOfPlaces"] > 12

    def test_limite_n_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_12_5"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_n_Purchase_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_12_6"
        club_email = "test_club@email.com"
        places = 12

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - reservation de n (n<12) places et club["points"] = n et competitions["numberOfPlaces"] > 12

    def test_limite_ncompet_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_10_1"
        places = 10

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_ncompet_Purchase_data(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_10_2"
        club_email = "test_club@email.com"
        places = 10

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # - date == aujourd'hui (la competition n'a pas commencée)

    def test_limite_Date_Purchase_HTTPcode(self):  # TEST LIMIT --> ça doit marcher

        competition = "Purchase_TestUnitaire_limit"
        club = "Purchase_Test_club"
        places = 7

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 200)

    def test_limite_Date_Purchase_data(self):  # TEST LIMIT --> ça doit marcher
        # on choisit un mail correct
        competition = "Purchase_TestUnitaire_limit"
        club = "Purchase_Test_club"
        club_email = "test_club@email.com"
        places = 7

        print(" **SI ERROR : change date to today in Purchase_TestUnitaire_limit**")
        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    #     CAS ERREURS
    #     x la competition n'existe pas

    def test_erreur_competition_not_exist_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher
        competition = ""
        club = "Purchase_Test_club"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertEqual(result.status_code, 404)

    def test_erreur_competition_not_exist_Purchase_data(self):  # TEST ERREURSL --> ça doit marcher
        # on choisit un mail correct
        competition = ""
        club = "Purchase_Test_club"
        club_email = "test_club@email.com"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club,
                                                           "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    # la competition est vide.

    def test_competition_not_send_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher
        club = "Purchase_Test_club"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club})
        self.assertEqual(result.status_code, 404)

    def test_competition_not_send_Purchase_data(self):  # TEST ERREURS --> ça doit marcher
        # on choisit un mail correct
        club = "Purchase_Test_club"
        club_email = "test_club@email.com"
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club})
        self.assertIn(club_email, result.data.decode())  # page welcome

    #     x le club n'existe pas

    def test_club_not_exist_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher
        competition = "Purchase_TestUnitaire_open"
        club = ""
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 401)

    def test_club_not_exist_Purchase_data(self):  # TEST ERREURS --> ça doit marcher
        competition = "Purchase_TestUnitaire_open"
        club = ""
        club_email = ""
        places = 1

        result = self.client.post("/purchasePlaces", data={"places": places, "club": club, "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    #     x le club n'est pas envoyé

    def test_club_not_send_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher
        competition = "Purchase_TestUnitaire_open"
        club = ""
        places = 1

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "competition": competition})
        self.assertEqual(result.status_code, 404)

    def test_club_not_send_Purchase_data(self):  # TEST ERREURS --> ça doit marcher
        competition = "Purchase_TestUnitaire_open"
        club = ""
        club_email = ""
        places = 1

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "competition": competition})
        self.assertIn(club_email, result.data.decode())  # page welcome

    #     x reservation de + de 12 places (13)

    def test_club_more_place_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open"
        club = "Purchase_Test_club"
        places = 13

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 401)

    def test_club_more_place_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open"
        club = "Purchase_Test_club"
        places = 13

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x reservation de place pour un concours qui est complet

    def test_competition_full_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full"
        club = "Purchase_Test_club"
        places = 8

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 410)

    def test_competition_full_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full"
        club = "Purchase_Test_club"
        places = 8

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x reservation de place pour un concours où competitions["numberOfPlaces"] < nbPlacesDemandées

    def test_8_over_5_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club"
        places = 8

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 412)

    def test_8_over_5_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club"
        places = 8

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x reservation mais pas assez de points nbPlacesDemandées > club["points"]

    def test_1_over_5_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_limit"
        places = 5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 412)

    def test_1_over_5_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_full_418"
        club = "Purchase_Test_club_limit"
        places = 5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x competition est finie

    def test_competition_close_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_closed"
        club = "Purchase_Test_club_limit"
        places = 5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 410)

    def test_competition_close_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_closed"
        club = "Purchase_Test_club_limit"
        places = 5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x le nombre de places demandées n'est pas un entier

    def test_number_is_float_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = 1.5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 401)

    def test_number_is_float_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = 1.5

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x le nombre de placse demandée est nul

    def test_place_null_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = 0

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 401)

    def test_place_null_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = 0

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    #     x le nombre de places demandée est négatif

    def test_place_negative_Purchase_HTTPcode(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = -1

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertEqual(result.status_code, 401)

    def test_place_negative_Purchase_data(self):  # TEST ERREURS --> ça doit marcher

        competition = "Purchase_TestUnitaire_open_5"
        club = "Purchase_Test_club_limit"
        places = -1

        result = self.client.post("/purchasePlaces",
                                  data={"places": places, "club": club, "competition": competition})
        self.assertIn(competition, result.data.decode())  # page booking

    def tearDown(self):  # after testing
        pass
