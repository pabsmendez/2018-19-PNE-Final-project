import http.server
import socketserver
from seq import Seq

PORT = 8004


def doing_operations(msg):
    processes = {}
    msg = msg.split("&")
    print(msg , 90)
    seq = Seq(msg.pop(0).split("=")[-1].upper())
    print(seq.strbases, "ok")
    bases = "ACTG"

    # Check if the characters of the DNA sequence are all allowed
    if not all(a in bases for a in seq.strbases):
        processes = "ERROR"
        return processes

    processes.update({"Seq": seq.strbases})
    # The function makes the computations
    base = ""
    print(msg)
    for request in msg:
        print(request)
        if "base" in request:
            base += request[-1]
        elif "count" in request:
            operation = request.split("=")[-1]
            print(operation)
            process = seq.count(base)
            processes.update({"Result for " + base + " " + operation: process})
        elif "percentage" in request:
            operation = request.split("=")[-1]
            process = seq.percentage(base)
            processes.update({"Result for " + base + " " + operation: process})
        elif request == "chk=on":
            process = seq.len()
            processes.update({"Len": process})

    return processes


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # -- printing the request  line
        #termcolor.cprint(self.requestline, "green")
        demand = self.requestline.split()[1]
        print(demand)
        progresses = demand.split("?")[-1]
        print(progresses)

        if self.path.startswith("/seq"):
            test = doing_operations(progresses)
            if test == "ERROR":
                f = open("error.html", 'r')
                contents = f.read()
                f.close()
            else:
                final_values = ""
                for key, value in test.items():
                    final_values += "<p>" + key + " : " + str(value) + "</p>"

                contents = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Results obtained</title>
                            </head>
                            <body>
                             <h1>Result of operations</h1>
                              {}
                              <a href="/">Main page</a>
                            </body>
                            </html>""".format(final_values)

        elif self.path == "/" or self.path == "/favicon.ico":
            f = open("form.html", 'r')
            contents = f.read()
            f.close()

        else:
            f = open("error_P6.html", 'r')
            contents = f.read()
            f.close()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
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