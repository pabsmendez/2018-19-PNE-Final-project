# Example of getting information stored in github

import http.client
import json
import socketserver

# -- API information
HOSTNAME = "rest.ensembl.org"
ENDPOINT = "/info/species?", "/karyotype", "/chromosomeLength", "/"
Action = input("name in github: ")
METHOD = "GET"

# -- Here we can define special headers if needed
headers = {'User-Agent': 'http-client'}

# -- Connect to the server
# -- NOTICE it is an HTTPS connection!
# -- If we do not specify the port, the standar one
# -- will be used
conn = http.client.HTTPSConnection(HOSTNAME)

# -- Send the request. No body (None)
# -- Use the defined headers
def do_GET(self):
    socketserver.TCPServer.allow_reuse_address = True

    if 'listSpecies' in self.path:
        conn.request(METHOD, ENDPOINT[0] + Action, None, headers)

        # -- Wait for the server's response
        r1 = conn.getresponse()

        # -- Print the status
        print()
        print("Response received: ", end='')
        print(r1.status, r1.reason)

        # -- Read the response's body and close
        # -- the connection
        text_json = r1.read().decode("utf-8")
        conn.close()
    else:
        conn.request(METHOD, ENDPOINT[1] + Action, None, headers)

        # -- Wait for the server's response
        r2 = conn.getresponse()

        # -- Print the status
        print()
        print("Response received: ", end='')
        print(r2.status, r2.reason)

        # -- Read the response's body and close
        # -- the connection
        text_json2 = r2.read().decode("utf-8")
        conn.close()

    user = json.loads(text_json)