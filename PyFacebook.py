import urllib
import urllib2
import cgi
import json
import ConfigParser

import facebook

class PyFacebook:


    def __init__(self, config_fname = '.config'):

        self.conf_fname = config_fname
        self.get_config()
        if self.app_code == 'None':
            self.authorize()

        self.authenticate()

        self.graph = facebook.GraphAPI(self.token)

    def get_config(self):

        config = ConfigParser.ConfigParser()
        config.read(self.conf_fname)

        self.app_id = config.get('AppInfo', 'app_id')
        self.app_secret = config.get('AppInfo', 'app_secret')
        self.app_code = config.get('AppInfo', 'code')


    def authenticate(self):
    
        url = 'https://graph.facebook.com/oauth/access_token'
        redirect_uri = 'http://www.facebook.com/connect/login_success.html'
    
        post_data = urllib.urlencode([
            ('redirect_uri', redirect_uri),
            ('client_id', self.app_id),
            ('client_secret', self.app_secret),
            ('code', self.app_code),
      ])

        request = urllib2.Request(url, post_data)
        response = urllib2.urlopen(request)

        content = '&'.join(response.read().split())
        query = cgi.parse_qs(content)
        self.token = query['access_token'][0]

        response.close()

    def authorize(self):
        print 'dss'
        url = 'https://graph.facebook.com/oauth/authorize'
        redirect_uri = 'http://www.facebook.com/connect/login_success.html'
    
        post_data = urllib.urlencode([
            ('redirect_uri', redirect_uri),
            ('client_id', self.app_id),
            ('scope', 'offline_access,read_stream,user_location,friends_location'),
        ])

        request = urllib2.Request(url, post_data)
        response = urllib2.urlopen(request)

        content = '&'.join(response.read().split())
        query = cgi.parse_qs(content)
        self.code = query['code'][0]

        response.close()

        #write it to config
        config = ConfigParser.ConfigParser()
        config.read(self.conf_fname)
        config.set('AppInfo', 'code', self.code)



def main():

    fb = PyFacebook()
    
    #api_id, api_secret, code = Config('.config')
    #token = authenticate(api_id, api_secret, code)
    #graph = facebook.GraphAPI(token)
    graph = fb.graph
    print graph.get_object("me")['first_name']
    print graph.get_connections("me", "friends")


if __name__ == '__main__':
    main()



#https://graph.facebook.com/oauth/authorize?redirect_uri=http://www.facebook.com/connect/login_success.html&client_id=149502475102187&scope=offline_access,read_stream,user_location,friends_location,read_friendlists

