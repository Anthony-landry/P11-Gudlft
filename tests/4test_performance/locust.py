#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Importation du la librairie Locust pour effet des tests de performances.
from locust import HttpUser, task, between
# import du fichier utils pour récuperer "loadClubs, loadCompetitions"
from utils import loadClubs, loadCompetitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)
    competition = loadCompetitions()[0]
    club = loadClubs()[0]

    @task
    def on_start(self):
        self.client.get("/", name=".index")
        self.client.post("/showSummary", data={'email': self.club["email"]}, name=".show_summary")

    @task
    def get_booking(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="book"
        )

    @task
    def post_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club["name"],
                "competition": self.competition["name"]
            },
            name="purchase_places"
        )
        # have some fail test with 412 http error because club have limited points

    @task
    def get_board(self):
        self.client.get("/displayPoints", name="displayPoints")
