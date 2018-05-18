from http import server


TEMPLATE = """<html>
<head>
    <link rel="stylesheet" type="text/css"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
    </link>
    <link rel="stylesheet" type="text/css"
          href="https://bootswatch.com/4/darkly/bootstrap.css">
    </link>
</head>

<body>

<div class="jumbotron">
    <h1 class="display-4">Hello world!</h1>
    <p class="lead">This illustrates the power of Bootstrap.</p>
    <hr class="my-4">
    <p>It allows you to quickly create beautiful pages.</p>
    <a class="btn btn-primary btn-lg" href="#" role="button">Tell me more</a>
</div>

</html>
"""

class RequestHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(TEMPLATE.encode("utf-8"))


server.test(RequestHandler, server.HTTPServer, port=8001, bind="0.0.0.0")
