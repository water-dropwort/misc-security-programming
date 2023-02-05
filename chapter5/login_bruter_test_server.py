import http.server
import http
import io
import urllib.parse

class TestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "test1"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        self._send_html("login_bruter_test_server_html/login.html")

    def do_POST(self):
        length = self.headers.get("content-length")
        nbytes = int(length)
        postdata = self.rfile.read(nbytes).decode("utf-8")
        parsed_postdata = urllib.parse.parse_qs(postdata)
        name = parsed_postdata["username"][0]
        pswd = parsed_postdata["password"][0]

        if "test.tarou@example.com" == name and "tarou0101" == pswd:
            self._send_html("login_bruter_test_server_html/login_succ.html")
        else:
            self._send_html("login_bruter_test_server_html/login_fail.html")

    def _send_html(self, htmlpath):
        html_text = None
        with open(htmlpath     , "r", encoding="utf-8") as f:
            html_text = f.read().encode("utf-8")
        
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type",   "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_text)))
        self.end_headers()
        self.wfile.write(html_text)

def run_server(port=1234):
    handler = TestHandler
    with http.server.HTTPServer(('', port), handler) as httpd:
        httpd.serve_forever()
    
    
