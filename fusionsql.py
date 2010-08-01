"""
Connection client for FusionTables
==================================

simple connector for fusion tables using OAuth,

Modifications and additions, copyright 2010 Dan Colish

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.  

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the name of the Dan Colish nor the names of its contributors may be used
to endorse or promote products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


I borrowed a lot from the older `OAuth example`_ which is copyright 2007 Leah
Culver

The MIT License

Copyright (c) 2007 Leah Culver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

.. _`OAuth Example`: http://github.com/simplegeo/python-oauth2/blob/master/example/client.py

"""
import csv
from ConfigParser import SafeConfigParser
from sys import argv
import oauth2 as oauth
import time
import httplib


def access_resource(oauth_request):
    connection = httplib.HTTPConnection('tables.googlelabs.com')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    connection.request('POST', '/api/query',
                       body=oauth_request.to_postdata(), headers=headers)
    response = connection.getresponse()
    return response.read()


config = SafeConfigParser()
config.read('fusiontable.cfg')

token = oauth.Token(key=config.get('auth', 'oauth_token'),
                    secret=config.get('auth', 'oauth_token_secret'))
consumer = oauth.Consumer(key="anonymous", secret="anonymous")
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
url = 'http://tables.googlelabs.com/api/query'

params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
}

params['oauth_token'] = token.key
params['oauth_consumer_key'] = consumer.key
params.update(**dict(sql=argv[1:].pop()))

oauth_request = oauth.Request.from_consumer_and_token(consumer,
                                                           token=token,
                                                           http_method='POST',
                                                           http_url=url,
                                                           parameters=params)
oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)

try:
    from tableformatter import indent
    reader = csv.reader(access_resource(oauth_request).splitlines())
    print indent(reader, hasHeader=True)

except Exception, e:
    print e
    raise Exception(e)
