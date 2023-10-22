#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import server
from server import app

PATH_TO_MAIN = "../"
"""
    Données en entrée : email
     1) pas d'email
     2) email vide
     3) pas le bon email (inconnu)
     4) email valide (connu)
    """


class ShowSummaryTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):  # before testing
        pass

    def test_validEmail_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher

        club = server.clubs[0]
        email = club["email"]

        result = self.client.post("/showSummary", data={"email": email})
        self.assertEqual(result.status_code, 200)

    def test_validEmail_data(self):  # TEST NOMINAL --> ça doit marcher

        club = server.clubs[0]
        email = club["email"]

        result = self.client.post("/showSummary", data={"email": email})
        self.assertIn(email, result.data.decode())  # page welcome

    def test_emailEmpty_HTTPcode(self):  # TEST D'ERREUR --> ca ne doit pas marché
        result = self.client.post("/showSummary", data={"email": ""})
        self.assertEqual(result.status_code, 401)

    def test_emailEmpty_data(self):  # TEST D'ERREUR --> ca ne doit pas marché
        result = self.client.post("/showSummary", data={"email": ""})
        self.assertIn("<title>GUDLFT Registration</title>", result.data.decode())  # page index

    def test_noEmail_HTTPcode(self):  # TEST D'ERREUR --> ca ne doit pas marché
        result = self.client.post("/showSummary", data={})
        self.assertEqual(result.status_code, 401)

    def test_noEmail_data(self):  # TEST D'ERREUR --> ca ne doit pas marché
        result = self.client.post("/showSummary", data={})
        self.assertIn("<title>GUDLFT Registration</title>", result.data.decode())  # page index

    def test_invalidEmail_HTTPcode(self):  # TEST D'ERREUR --> ca ne doit pas marché
        # pas dans la bdd
        email = "test@1.fr"

        result = self.client.post("/showSummary", data={"email": email})
        self.assertEqual(result.status_code, 403)

    def test_invalidEmail_data(self):  # TEST D'ERREUR --> ca ne doit pas marché
        email = "test@1.fr"

        result = self.client.post("/showSummary", data={"email": email})
        self.assertIn("<title>GUDLFT Registration</title>", result.data.decode())  # page index

    def tearDown(self):  # after testing
        pass
