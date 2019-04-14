import http.server
import socketserver
# -- from seq import Seq
import termcolor
import requests
# -- import sys
PORT = 8000
ENDPOINTS = "info/species"
SERVER = "http://rest.ensembl.org/"
header = {"Content-Type": "application/json"}
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # -- printing the request  line.
        termcolor.cprint(self.requestline, "green")

        # -- to detect which is the correct path.
        if self.path == "/" or self.path == "/favicon.ico":
            f = open("form.html", 'r')
            contents = f.read()
            f.close()
        elif "listSpecies" in self.path:
            extension = ENDPOINTS
            r = requests.get(SERVER + extension, headers=header)
            # -- if not r.ok:r.raise_for_status() sys.exit()
            decode = r.json()
            # -- this exception action is to avoid an error when you write directly the limit in the browser
            # or you only write the request /listSpecies.
            try:
                if 'json=1' in self.path:
                    limit = self.path.split("=")[1].split("&")[0]
                else:
                    limit = self.path.split("=")[1]
            except IndexError:
                limit = 199

            # -- to avoid a problem when you don't apply a limit.
            if limit == "":
                limit = len(decode['species'])
            join = ''

            # -- to write only the part of the listSpecies that we want from the API
            # as many times as the client decide with the limit parameter.
            for i in range(int(limit)):
                join += "<li>" + 'scientific name:{},  \n common name: {}\n\n'\
                    .format(decode['species'][i]['name'], decode['species'][i]['common_name'])

            contents = str(join)

        else:
            f = open("error.html", 'r')
            contents = f.read()
            f.close()

        self.send_response(200)

        self.send_header('Content-Type', 'Text/HTML')
        self.send_header('Content-length', len(str.encode(contents)))
        self.end_headers()

        # -- Sending the body of the response message
        self.wfile.write(str.encode(contents))


# -- Main programme
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {} ".format(PORT))
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.server_close()

print("The server is stopped")
