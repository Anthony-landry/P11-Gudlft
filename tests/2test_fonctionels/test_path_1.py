#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import unittest
import time

from .const import GUDLFT_DRIVER_PATH


class TestPathPurchasePlacesFull(unittest.TestCase):
    def setUp(self):
        self.titleEndScenario = "GUDLFT Registration"

    def test_Fonctionnel_should_connect_book_and_see_welcome_page(self):
        env = os.environ.copy()
        env["FLASK_APP"] = "server"
        server = subprocess.Popen(['flask', 'run', '--port', "5000"], env=env)

        # route / --> index.html connection
        my_webdriver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))
        my_webdriver.get(GUDLFT_DRIVER_PATH)
        self.sleeping()
        input_email = my_webdriver.find_element(webdriver.common.by.By.NAME, "email")
        input_email.send_keys("maxbestclub@email.com")
        self.sleeping()
        input_email.send_keys(webdriver.common.keys.Keys.ENTER)
        self.sleeping()

        # route /showSummary --> welcome.html affichage des compet et choix d'une compet ouverte
        link_to_book = my_webdriver.find_element(webdriver.common.by.By.ID, "Purchase_TestUnitaire_open_full_418")
        link_to_book.click()
        self.sleeping()

        # route /book --> page book
        input_places = my_webdriver.find_element(webdriver.common.by.By.NAME, "places")
        input_places.send_keys("1")
        self.sleeping()
        input_places.send_keys(webdriver.common.keys.Keys.ENTER)
        self.sleeping()

        # route /purchasePlaces --> welcome
        logout = my_webdriver.find_element(webdriver.common.by.By.ID, "logout")
        self.sleeping()
        logout.click()

        title = my_webdriver.find_element(webdriver.common.by.By.TAG_NAME, "title")
        self.assertEqual(self.titleEndScenario, title.get_attribute('innerHTML'))

        if my_webdriver is not None:
            my_webdriver.close()
            my_webdriver.quit()

        server.terminate()

    @staticmethod
    def sleeping():
        return time.sleep(0)

    def tearDown(self):
        pass
