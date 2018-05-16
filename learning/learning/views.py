import os
import signal
import subprocess
import sys
from collections import OrderedDict
from time import sleep

import psutil

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView


MODULES_PATH = os.path.join(settings.BASE_DIR, "..", "modules")
pid = None


class Home(TemplateView):
    template_name = "learning/home.html"

    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs):
        di = super().get_context_data(**kwargs)
        modules = OrderedDict()
        for module in os.listdir(MODULES_PATH):
            if module.endswith(".py"):
                buf = open(os.path.join(MODULES_PATH, module), "r").read()
                modules[module[:-3]] = buf
        modules["scratchpad"] = ""
        di["modules"] = modules
        return di

    def post(self, request, *args, **kwargs):
        global pid
        data = request.POST
        name = data["name"]

        if "run" in data:

            # Kill possible old server
            if pid is not None:
                os.kill(pid, signal.SIGTERM)

            # Write a run file
            fname = os.path.join(MODULES_PATH, name) + ".py.run"
            fp = open(fname, "w")
            try:
                fp.write(data["content"])
            finally:
                fp.close()

            context = self.get_context_data(**kwargs)

            # Run the code
            try:
                proc = subprocess.run(
                    [sys.executable, fname],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=1
                )
            except subprocess.TimeoutExpired:
                # This is probably a server
                output = "Server detected"
                proc = subprocess.Popen(
                    [sys.executable, fname]
                )
                sleep(1)
                pid = proc.pid
                p = psutil.Process(pid)
                connections = p.connections()
                if connections:
                    context["server"] = "http://%s:%s" % (
                        request.get_host().split(":")[0],
                        connections[0].laddr.port
                    )
            else:
                if proc.returncode == 0:
                    output = proc.stdout.decode("utf-8")
                else:
                    output = proc.stderr.decode("utf-8")

            # Update context
            context["modules"][name] = data["content"]
            context["output"] = output

            return HttpResponse(
                render_to_string(self.template_name, context=context, request=request)
            )

        if "save" in data:
            if name == "scratchpad":
                name = str(len(os.listdir(MODULES_PATH)) + 1)
            fname = os.path.join(MODULES_PATH, name) + ".py"
            fp = open(fname, "w")
            try:
                fp.write(data["content"])
            finally:
                fp.close()
            return HttpResponseRedirect(reverse("home"))
