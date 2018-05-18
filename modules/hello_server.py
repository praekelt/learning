from http import server


class RequestHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(b"Hello world!")


server.test(RequestHandler, server.HTTPServer, port=8001, bind="0.0.0.0")
