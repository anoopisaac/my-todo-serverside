from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urllib
import json



class S(BaseHTTPRequestHandler):
    app_id = "288727298296356"
    app_secret = "c316f5bcb0b28c1012cd6ce759af320e"
    
    def _set_headers(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def get_json_response(self, url):
        """
        Parse the access token from Facebook's response
        Args:
            uri: the facebook graph api oauth URI containing valid client_id,
                redirect_uri, client_secret, and auth_code arguements
        Returns:
            a string containing the access key 
        """
        token = str(urllib.urlopen(url).read()).encode("utf-8")
        print token
        json_resp = json.loads(token)
        return json_resp;

    def do_GET(self):
        
        if 'code' in self.path:
            auth_code = self.path.split('=')[1]
            json_resp = self.get_json_response(
                self.GRAPH_API_AUTH_URI + auth_code)
            json_resp = self.get_json_response(
                self.FACEBOOK_GRAPH_API_ME + json_resp["access_token"])
            self.email=json_resp["email"]
            self.send_response(302)
            self.send_header('Location', "http://localhost/eee")
            self.end_headers()
        else:
            self._set_headers()
            self.wfile.write("<html><body><a href='https://www.facebook.com/dialog/oauth?client_id=288727298296356&redirect_uri=" +
                             self.REDIRECT_URL + "&scope=email'>facebook "+self.email+"</a></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    handler_class.FACEBOOK_GRAPH_API_ME="https://graph.facebook.com/v2.5/me?fields=email&access_token="
    handler_class.REDIRECT_URL = 'http://hello12345.test.com/'
    handler_class.GRAPH_API_AUTH_URI = ('https://graph.facebook.com/v2.2/oauth/'
                                   + 'access_token?client_id=' + handler_class.app_id + '&redirect_uri='
                                   + handler_class.REDIRECT_URL + '&client_secret=' + handler_class.app_secret + '&code=')
    handler_class.email="hello"
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
