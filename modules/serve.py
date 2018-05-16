from http import server


class RequestHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
      s = self

      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()

      s.wfile.write(b"hello")

      # and then the index file
      #s.wfile.write(open("index.html").read())


server.test(RequestHandler, server.HTTPServer, port=8001, bind="0.0.0.0")
