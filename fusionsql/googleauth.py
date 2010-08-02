"""
Google OAuth Client
===================

copyright 2010 Dan Colish <dcolish@gmail.com>
See LICENSE for more detail
"""

from ConfigParser import SafeConfigParser
from urllib import urlencode

import urlparse
import oauth2 as oauth


class GoogleOauth(object):

    request_token_url = 'https://www.google.com/accounts/OAuthGetRequestToken'
    access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'
    authorize_url = 'https://www.google.com/accounts/OAuthAuthorizeToken'

    def __init__(self, consumer_key='anonymous',
                 consumer_secret='anonymous'):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.consumer = oauth.Consumer(self.consumer_key,
                                       self.consumer_secret)
        self.client = oauth.Client(self.consumer)

    def authorize(self, scope):
        url = self.request_token_url + "?" + urlencode(dict(scope=scope),
                                                       True)
        resp, content = self.client.request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s,  %s." % (resp['status'],
                                                           content))
        request_token = dict(urlparse.parse_qsl(content))
        print "Go to the following link in your browser:"
        print "%s?oauth_token=%s" % (self.authorize_url,
                                     request_token['oauth_token'])
        print

        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')

        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(self.access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))

        self.write_config(access_token)

    def write_config(self, access_token):
        config = SafeConfigParser()
        config.add_section('auth')
        config.set('auth', 'oauth_token', access_token['oauth_token'])
        config.set('auth', 'oauth_token_secret',
                   access_token['oauth_token_secret'])

        with open('auth.cfg', 'wb') as configfile:
            config.write(configfile)
