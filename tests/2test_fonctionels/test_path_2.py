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


class TestPathDisplayPointl(unittest.TestCase):
    def setUp(self):
        self.titleEndScenario = "Club's Points | GUDLFT"

    def test_Fonctionnel_should_connect_book_and_see_welcome_page(self):
        env = os.environ.copy()
        env["FLASK_APP"] = "server"
        server = subprocess.Popen(['flask', 'run', '--port', "5000"], env=env)

        # route /displayPoints --> displayPoints.html
        my_webdriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        my_webdriver.get(GUDLFT_DRIVER_PATH + "displayPoints")
        self.sleeping()

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
