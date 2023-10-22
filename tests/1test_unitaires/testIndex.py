#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from server import app


class IndexTestCase(unittest.TestCase):
    client = app.test_client()

    def setUp(self):  # before testing
        pass

    def test_index_HTTPcode(self):  # TEST NOMINAL --> ça doit marcher
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_index_data(self):  # TEST NOMINAL --> ça doit marcher
        result = self.client.get("/")
        self.assertIn("<title>GUDLFT Registration</title>", result.data.decode())  # page index

    def tearDown(self):  # after testing
        pass
