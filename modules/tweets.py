import os
from http import server

import twitter
from jinja2 import Template


TEMPLATE = """<html>
<head>
    <link rel="stylesheet" type="text/css"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
     </link>
</head>

<body>

{% for status in statuses %}
    <div class="alert alert-secondary" role="alert">
        {% if status.retweeted_status %}
            <img class="rounded" src="{{ status.retweeted_status.user.profile_image_url }} "/>
        {% else %}
            <img class="rounded" src="{{ status.user.profile_image_url }} "/>
        {% endif %}
        <p>{{ status.text }}</p>
    </div>
{% endfor %}

</html>
"""


def render(**kwargs):
    template = Template(TEMPLATE)
    return template.render(**kwargs)


def get_statuses(screen_name="LFC"):
    # Read the config file
    try:
        buf = open(os.path.join(os.path.expanduser("~"), "tweets.conf"), "r").read()
    except IOError:
        raise RuntimeError("Unable to read tweets.conf")

    # Optimistic parse
    consumer_key, consumer_secret, access_token_key, access_token_secret = \
        buf.strip("\n").split("\n")

    # Setup API and fetch tweets
    api = twitter.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret
    )
    statuses = api.GetUserTimeline(screen_name=screen_name)
    return statuses[:5]


class RequestHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(render(statuses=get_statuses("praekelt")).encode("utf-8"))


server.test(RequestHandler, server.HTTPServer, port=8001, bind="0.0.0.0")
