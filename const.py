#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
mettre le parametre **test** à *True* afin que le programme selectionne les bons fichiers de data
"""

test = True

TEST = ''
TEST2 = ''
if test:
    TEST = "_test"
    TEST2 = "_save"

FILE_CLUB = 'clubs' + TEST + '.json'
FILE_COMPETITION = 'competitions' + TEST + '.json'

FILE_CLUB_SAVE = 'clubs' + TEST2 + '.json'
FILE_COMPETITION_SAVE = 'competitions' + TEST2 +'.json'
