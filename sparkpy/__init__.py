# -*- coding: utf-8 -*-
'''
.. module:: pyspark
   :platform: Python 3.6.2, Cisco Spark
   :synopsis: A python API wrapper for Cisco Spark APIs
.. moduleauthor:: Paul Anholt <panholt@gmail.com>
'''

import logging
from .spark import Spark
from .models.file import SparkFile
from .models.license import SparkLicense
from .models.message import SparkMessage
from .models.organization import SparkOrganization
from .models.people import SparkPerson
from .models.role import SparkRole
from .models.room import SparkRoom
from .models.team import SparkTeam
from .models.webhook import SparkWebhook
from .models.membership import SparkMembership, SparkTeamMembership

__all__ = ['Spark',
           'SparkFile',
           'SparkLicense',
           'SparkMembership',
           'SparkMessage',
           'SparkOrganization',
           'SparkPerson',
           'SparkRole',
           'SparkTeam',
           'SparkTeamMembership',
           'SparkWebhook']
