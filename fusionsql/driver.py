# Copyright 2010 Dan Colish
# All rights reserved.
#
# This file is part of 'fusionsql' and is distributed under the BSD license.
# See LICENSE for more details.
"""
Connection client for FusionTables
==================================

simple client for fusion tables using OAuth

copyright 2010 Dan Colish <dcolish@gmail.com>

See LICENSE for more detail
"""

import csv
from ConfigParser import SafeConfigParser
from oauth2 import (
    Consumer,
    generate_nonce,
    Request,
    SignatureMethod_HMAC_SHA1,
    Token,
)
import time
import httplib
from tableformatter import indent


class QueryException(Exception):
    """Raised when query returns abnormally"""
    pass


class FusionSQL(object):

    oauth_params = {
        'oauth_version': "1.0",
        'oauth_nonce': generate_nonce(),
        'oauth_timestamp': int(time.time()),
        }
    signature_method_hmac_sha1 = SignatureMethod_HMAC_SHA1()
    url = 'http://tables.googlelabs.com/api/query'
    config = SafeConfigParser()

    def __init__(self):
        self.tables = {}
        self.config.read('auth.cfg')
        if not self.config.sections():
            from googleauth import GoogleOauth
            gauth = GoogleOauth()
            gauth.authorize(self.url)
            self.config.read('auth.cfg')

        self.token = Token(key=self.config.get('auth', 'oauth_token'),
                                 secret=self.config.get('auth',
                                                   'oauth_token_secret'))
        self.consumer = Consumer(key="anonymous", secret="anonymous")

        self.oauth_params['oauth_token'] = self.token.key
        self.oauth_params['oauth_consumer_key'] = self.consumer.key

    def access_resource(self, oauth_request):
        connection = httplib.HTTPConnection('tables.googlelabs.com')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        connection.request('POST', '/api/query',
                           body=oauth_request.to_postdata(), headers=headers)
        response = connection.getresponse()
        if response.status == 200:
            return response.read()
        else:
            raise QueryException("Response: %d, %s" % (response.status,
                                                  response.reason))

    def query(self, query, pprint=False):
        self.oauth_params.update({'sql': query})
        oauth_request = Request.from_consumer_and_token(
            self.consumer, token=self.token, http_method='POST',
            http_url=self.url, parameters=self.oauth_params)
        oauth_request.sign_request(self.signature_method_hmac_sha1,
                                   self.consumer, self.token)
        return self.parse(self.access_resource(oauth_request).splitlines(),
                          pprint)

    def parse(self, response, pprint):
        try:

            if pprint:
                reader = csv.reader(response)
                return indent([x for x in reader], hasHeader=True)
            else:
                return csv.DictReader(response)
        except Exception, e:
            print e
            raise Exception(e)

    def build_tables(self):
        for table in self.query("SHOW TABLES"):
            table_columns = self.query("DESCRIBE %s" % table['table id'])
            table_attrs = {'name': table['name'],
                           'columns': list(x for x in table_columns)}
            self.tables.update({table['table id']: table_attrs})
