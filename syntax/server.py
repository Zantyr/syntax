import argparse
import flask   # migrate to bottle
import json
import os
import re
import subprocess
import tempfile


class DropInServer:
    """
    Minimalistic server that given config will call proper subprocesses and get their input
    Should reload config dynamically whenever it is changed if file is given
    Should be installable and runnable via cli method

    TODO: autoparams (not handcrafted)
    """

    _default_cfg_path = os.path.join(os.path.expanduser("~"), ".local", ".syntax.dropin.json")
    _parser = argparse.ArgumentParser()
    _parser.add_argument("--run", action="store_true", help="Run the DropIn server")
    _parser.add_argument("--make_config", action="store_true", help="Build default config in your home")
    

    def __init__(self, config_path=None, config=None):
        if config:
            self.config = config
        else:
            if config_path is None:
                config_path = DropInServer._default_cfg_path
            with open(config_path, "r") as f:
                self.config = json.load(f)
        self.endpoints =  self.config["endpoints"]
        if not self.endpoints:
            raise RuntimeError("No endpoints - terminating")
        self.app = flask.Flask(__name__)
        @self.app.route('/<page>', methods=["GET", "POST"])
        def index(page):
            paths = []
            for epoint in self.endpoints:
                if page.startswith(epoint["route"]):
                    break
            else:
                flask.abort(404)
            if flask.request.method == 'POST':
                if flask.request.content_type == 'application/json':
                    data = flask.request.get_json()
                else:
                    data = flask.request.form
                for fobj in flask.request.files:
                    if fobj.filename:
                        path = tempfile.mkstemp()[1]
                        fobj.save(path)
            else:
                data = {}
            try:
                return self.call(epoint, page, data)
            finally:
                for path in paths:
                    os.remove(path)
        self.app.run(self.config["address"], self.config["port"])

    def call(self, epoint, page, data):
        call = []
        for bit in epoint["params"]:
            params = set(re.findall("\\$([A-Za-z]+|\\{w+?\\})", bit))
            if params:
                if all([x in data for x in params]):
                    for param in params:
                        bit = bit.replace("$" + param. data[param])
                    call.append(bit)
            else:
                call.append(bit)
        p = subprocess.Popen([epoint["executable"]] + call, stdout=subprocess.PIPE)
        response, error = p.communicate()
        if p.returncode:
            flask.abort(500, {'message': error})
        else:
            return response

    @classmethod
    def cli(cls, *args):
        args = cls._parser.parse_args(args)
        if args.run:
            return DropInServer()
        elif args.make_config:
            config = {
                "address": "0.0.0.0",
                "port": 2137,
                "endpoints": [
                    {
                        "route": "ls",
                        "executable": "ls",
                        "params": []
                    }
                ]
            }
            with open(cls._default_cfg_path, "w") as f:
                json.dump(config, f)
