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
from ConfigParser import SafeConfigParser
import csv
import time
import httplib

from oauth2 import (
    Consumer,
    generate_nonce,
    Request,
    SignatureMethod_HMAC_SHA1,
    Token,
)

from .exception import DatabaseError, OperationalError

apilevel = "2.0"
threadsafety = 0


def connect(dsn):
    return Connection(dsn)


class Connection(object):

    oauth_params = {
        'oauth_version': "1.0",
        'oauth_nonce': generate_nonce(),
        'oauth_timestamp': int(time.time()),
        }
    signature_method_hmac_sha1 = SignatureMethod_HMAC_SHA1()
    url = 'http://tables.googlelabs.com/api/query'
    config = SafeConfigParser()

    def __init__(self, dsn):
        self.tables = {}
        self.config.read('auth.cfg')
        if not self.config.sections():
            from googleauth import GoogleOauth
            gauth = GoogleOauth()
            gauth.authorize(self.url)
            self.config.read('auth.cfg')
        self.closed = False

        self.token = Token(key=self.config.get('auth', 'oauth_token'),
                                 secret=self.config.get('auth',
                                                   'oauth_token_secret'))
        self.consumer = Consumer(key="anonymous", secret="anonymous")
        self.oauth_params['oauth_token'] = self.token.key
        self.oauth_params['oauth_consumer_key'] = self.consumer.key
        self.connection = httplib.HTTPConnection('tables.googlelabs.com')

    def access_resource(self, query):
        self.oauth_params.update({'sql': query})
        oauth_request = Request.from_consumer_and_token(
            self.consumer, token=self.token,
            http_method='POST', http_url=self.url,
            parameters=self.oauth_params)
        oauth_request.sign_request(self.signature_method_hmac_sha1,
                                   self.consumer, self.token)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.connection.request('POST', '/api/query',
                                body=oauth_request.to_postdata(),
                                headers=headers)
        response = self.connection.getresponse()
        if response.status == 200:
            return response.read().splitlines()
        else:
            raise OperationalError("Response: %d, %s" % (response.status,
                                                  response.reason))

    def build_tables(self):
        for table in csv.DictReader(self.access_resource("SHOW TABLES")):
            table_columns = self.access_resource("DESCRIBE %s" %
                                                 table['table id'])
            table_attrs = {'name': table['name'],
                           'columns': list(x for x in table_columns)}
            self.tables.update({table['table id']: table_attrs})

    def close(self):
        if self.closed:
            raise DatabaseError("Database closed")
        self.connection.close()
        self.closed = True

    def commit(self):
        """There is no transactional support from FusionTables"""
        if self.closed:
            raise DatabaseError("Database closed")

    def cursor(self):
        if self.closed:
            raise DatabaseError("Database closed")
        return Cursor(self)


class Cursor(object):

    def __init__(self, connection):
        self.connection = connection
        self.arraysize = 1
        self.closed = False

    @property
    def describe(self):
        pass

    @property
    def rowcount(self):
        pass

    def close(self):
        if self.closed:
            raise OperationalError
        self.closed = True

    def execute(self, operation, parameters=None):
        if self.closed:
            raise OperationalError
        return self.connection.access_resource(operation)

    def executemany(operation, seq):
        pass

    def fetchone(self):
        pass

    def fetchmany(self, size=None):
        if not size:
            size = self.arraysize

    def fetchall(self):
        pass

    def nextset(self):
        pass

    def setinputsizes(sizes):
        pass

    def setoutputsize(size, columns=None):
        pass
