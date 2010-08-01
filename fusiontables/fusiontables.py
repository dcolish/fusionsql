from ConfigParser import SafeConfigParser
from urllib import urlencode

import urlparse
import oauth2 as oauth

consumer_key = 'anonymous'
consumer_secret = 'anonymous'
scope = "http://tables.googlelabs.com/api/query"
request_token_url = 'https://www.google.com/accounts/OAuthGetRequestToken'
access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'
authorize_url = 'https://www.google.com/accounts/OAuthAuthorizeToken'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

url = request_token_url + "?" + urlencode(dict(scope=scope), True)

print url
resp, content = client.request(url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s,  %s." % (resp['status'], content))

request_token = dict(urlparse.parse_qsl(content))
print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print

accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')

token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))

config = SafeConfigParser()
config.add_section('auth')
config.set('auth', 'oauth_token', access_token['oauth_token'])
config.set('auth', 'oauth_token_secret', access_token['oauth_token_secret'])

with open('fusiontable.cfg', 'wb') as configfile:
    config.write(configfile)
