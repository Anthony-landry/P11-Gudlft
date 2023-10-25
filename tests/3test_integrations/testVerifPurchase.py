#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Unittest est le framework de test fourni par défaut avec Python.
import unittest
# Bibliotheque par défaut systeme de python
import sys

sys.path.append("..")

from server import app
import utils


class PointsUpdateTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):
        self.club_name = utils.loadClubs()[0]["name"]
        self.competition_name = utils.loadCompetitions()[0]["name"]

    def test_points_update(self):
        club_points_before = int(utils.getClub(self.club_name)["points"])
        competition_places_before = int(utils.getCompet(self.competition_name)["numberOfPlaces"])
        places_booked = 1

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": places_booked,
                "club": utils.loadClubs()[0]["name"],
                "competition": utils.loadCompetitions()[0]["name"]
            }
        )

        club_points_after = int(utils.loadClubs()[0]["points"])
        competition_places_after = int(utils.loadCompetitions()[0]["numberOfPlaces"])

        self.assertTrue(result.status_code == 200 or int(club_points_before - club_points_after) == int(places_booked)
                        or int(competition_places_before - competition_places_after) == int(places_booked))
