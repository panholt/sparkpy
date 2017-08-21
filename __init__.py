# -*- coding: utf-8 -*-
'''
.. module:: pyspark
   :platform: Python 3.6.2, Cisco Spark
   :synopsis: A python API wrapper for Cisco Spark APIs
.. moduleauthor:: Paul Anholt <panholt@gmail.com>
'''

import logging
from .spark import Spark


logging.basicConfig(filename='sparkpy.log', filemode='w', level=logging.DEBUG)
