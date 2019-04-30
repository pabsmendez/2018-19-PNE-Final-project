import http.server
import socketserver
# -- from seq import Seq
import termcolor
import requests
# -- import sys
PORT = 8000
ENDPOINTS = "info/species", "info/assembly/", "/xrefs/symbol/homo_sapiens/{}", "/sequence/id/{}?expand=1"
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
            r = requests.get(SERVER + ENDPOINTS[0], headers=header)
            # -- if not r.ok:r.raise_for_status() sys.exit()
            decode = r.json()
            # -- this exception action is to avoid an error when you write directly the limit in the browser
            # or you only write the request /listSpecies.
            try:
                limit = self.path.split("=")[1].split("&")[0]
            except IndexError:
                limit = 199

            # -- to avoid a problem when you don't apply a limit.
            if limit == "":
                limit = len(decode['species'])
            join = "<body><h4> LIST OF SPECIES<body><h4> <a href='/'>link to the home page</a>"

            # -- to write only the part of the listSpecies that we want from the API
            # as many times as the client decide with the limit parameter.
            for i in range(int(limit)):
                join += "<li>" + 'scientific name:{},  \n common name: {}\n\n'\
                    .format(decode['species'][i]['name'], decode['species'][i]['common_name'])
            join += "<br><br> <a href='/'>link to the home page</a>"
            contents = str(join)
        elif "karyotype" in self.path:
            specie = self.path.split("=")[1]
            if specie:
                r = requests.get(SERVER + ENDPOINTS[1] + specie + '?', headers=header)

                decode = r.json()
                join = ''
                if r.ok:
                    join += "<body><h2>INFORMATION ABOUT THE KARYOTYPE<body><h2><a href='/'>link to the home page</a>" \
                            "<body><h3>The information of the karyotype" \
                            " of {} is: {}<body><h3>".format(specie, decode['karyotype'])
                else:
                    join = "<body><h2>INFORMATION ABOUT THE KARYOTYPE<body><h2><br><br>" \
                           "<body><h3>Sorry, return to the main page because you wrote an incorrect specie's " \
                           "name<body><h3> <a href='/'>link to the home page</a>"
            else:
                join = "<body><h2>INFORMATION ABOUT THE KARYOTYPE<body><h2><br><br>" \
                       "<body><h3>Sorry, You didn't write a specie's name, so return to the main page and" \
                       " please write one<body><h3> <a href='/'>link to the home page</a>"
            contents = str(join)
        elif "chromosomeLength" in self.path:
            specie = self.path.split("=")[1].split("&")[0]
            print(specie)
            chromo = self.path.split("&")[1].split("=")[1]
            print(chromo)
            if specie and chromo:
                r = requests.get(SERVER + ENDPOINTS[1] + specie + '/' + chromo + '?', headers=header)
                decode = r.json()
                join = ''
                if r.ok:
                    join += "<body><h2>INFORMATION ABOUT THE LENGTH OF CHROMOSOMES<body><h2><a href='/'>link " \
                            "to the home " \
                            "page</a>" + "<body><h3>The length of the" \
                            " {} chromosome of {}'s specie is:<body><h3>{} ".format(chromo, specie, decode["length"])
                else:
                    join = "<body><h2>INFORMATION ABOUT THE LENGTH OF CHROMOSOMES<body><h2> <br><br>" \
                           "<body><h3>Please you wrote wrong the fields of the request, return to the main page" \
                           " and try again<body><h3> <a href='/'>link to the home page</a>"
            else:
                join = "<body><h2>INFORMATION ABOUT THE LENGTH OF CHROMOSOMES<body><h2> <br><br>" \
                       "<body><h3>Please you forgot fill all the fields of the request, return to the main page" \
                       " and try again<body><h3> <a href='/'>link to the home page</a>"
            contents = str(join)
        elif "geneSeq" in self.path or "geneInfo" in self.path or "geneCalc" in self.path:
            gene = self.path.split("=")[1]
            join = ''
            if gene:
                r1 = requests.get(SERVER + ENDPOINTS[2].format(gene), headers=header)
                decode = r1.json()
                id = decode[0]['id']
                if "geneSeq" in self.path:
                    r2 = requests.get(SERVER + ENDPOINTS[3].format(id), headers=header)
                    id_decode = r2.json()
                    join += "<body><h1>Human's gene sequence</h1>" \
                            "<p style='word-break: break-all'>{}</p>".format(id_decode['seq'])
                elif "geneInfo" in self.path:
                    r2 = requests.get(SERVER + ENDPOINTS[3].format(id), headers=header)
                    id_decode = r2.json()
                    print(id_decode)
                    # -- we should split the id_decode to obtain the necessary iformation
                    info_needed = id_decode['desc'].split(':')
                    # -- depend on what we need inside info_needed we used the following variables
                    chromo = info_needed[3]
                    start = info_needed[2]
                    end = info_needed[4]
                    id = id_decode['id']
                    length = id_decode['id']

                    join += "<body><h1>Information about human's gene sequence</h1>" \
                            "Start: {} <br><br> End:{} <br><br> Length: {} <br><br> id: {} <br><br> Chromosome: {}"\
                        .format(start, end, length, id, chromo)
                elif "geneCalc" in self.path:
                    r2 = requests.get(SERVER + ENDPOINTS[3].format(id), headers=header)
                    id_decode = r2.json()
                    join = "yy"
                contents = str(join)
            else:
                join = "gfhuui"
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
