#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys

sys.path.append("..")

from server import app
import utils

PATH_TO_MAIN = "../"
"""
    Données en entrée : email
     1) pas d'email
     2) email vide
     3) pas le bon email (inconnu)
     4) email valide (connu)
    """


class DisplayPointTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):  # before testing
        pass

    def test_DisplayPoint_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher
        # on choisit un mail correct

        club = "Book_Test_club"

        result = self.client.get('/displayPoints')
        self.assertEqual(result.status_code, 200)

    def test_DisplayPoint_data(self):  # TEST NOMINAL --> ça doit marcher
        # on choisit un mail correct

        club = "Book_Test_club"

        pageHtml = self.client.get('/displayPoints')

        dataFromHtml = utils.extractClubsInfoFromDisplayPoint(pageHtml.data)
        dataFromBdd = utils.removeEmailToJSON()

        print(dataFromHtml)
        print(dataFromBdd)
        self.assertTrue(utils.checkIfExtractMailSameInJSON(dataFromHtml, dataFromBdd))  # page displayPoints

    def tearDown(self):  # after testing
        pass
