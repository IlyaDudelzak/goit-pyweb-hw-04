from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path
import urllib.parse
import mimetypes
import pathlib
import json

dataPath = Path("storage/data.json")
data = {}
if(dataPath.exists()):
    with open(dataPath, "r", encoding="utf-8") as f:
        data = json.load(f)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data_ = self.rfile.read(int(self.headers['Content-Length']))
        print(data_)
        data_parse = urllib.parse.unquote_plus(data_.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        print(type(str(datetime.now())))
        data[str(datetime.now())] = data_dict
        with open(dataPath, "w", encoding="utf-8") as f:
            json.dump(data, f)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())
        

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()

