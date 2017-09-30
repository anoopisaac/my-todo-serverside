from BaseHTTPServer  import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open_new
class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server):
        #self.app_id = a_id
        #self.app_secret = a_secret
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

class TokenHandler:
    """
    Class used to handle Facebook oAuth
    """
    def __init__(self):
        # self._id = a_id
        # self._secret = a_secret
        self.get_access_token()

    def get_access_token(self):
        httpServer = HTTPServer(('localhost', 8090),
                lambda request, address, server: HTTPServerHandler(request, address, server))
        httpServer.handle_request()

if __name__ == '__main__':
    handler= TokenHandler();
    handler.get_access_token();
    print("This only executes when %s is executed rather than imported" % __file__)