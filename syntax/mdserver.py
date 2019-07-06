#!/usr/bin/env python3

import atexit
import flask
import markdown
import os
import re
import requests
import threading

from functools import reduce



class AnalyticsSaver(object):
    def __init__(self, filename, interval):
        self.filename = filename
        self.lock = threading.Lock()
        self.list = []
        atexit.register(self.serialize)
        self.interval = interval
        self.thread = threading.Timer(interval, self.collect)
        self.thread.daemon = True
        self.thread.start()

    def append(self, request):
        with self.lock:
            self.list.append(request)

    def serialize(self):
        if not os.path.isfile(self.filename):
                os.mknod(self.filename)
        with open(self.filename, "a") as f:
            with self.lock:
                if self.list:
                    f.write(list(reduce(lambda a, b: a + b, ["{}\n".format(';'.join(x)) for x in self.list])))
                    self.list = []

    def collect(self):
        self.serialize()
        self.thread = threading.Timer(self.interval, self.collect)
        self.thread.daemon = True
        self.thread.start()


class CustomMarkdown(object):

    python_reserved_words = "and def assert break class continue del elif else except exec finally for from global if import in is lambda not or pass print raise return try while".split()

    def __init__(self):
        self.md = markdown.Markdown()

    def convert(self, text):
        codes = []
        text = re.sub('!\\[(.*)\\]\\((.*)\\)', "<img src='/bin/\\2' alt='\\1' class='enlargeable' />", text)
        code = re.findall('```([^`]*?)```',  text)
        for ix, match in enumerate(code):
            codes.append(self.python_highlight(match))
            text = text.replace("```{}```".format(match), '<!--CODE{}-->'.format(ix))
        text = self.md.convert(text)
        for ix, match in enumerate(codes):
            text = text.replace('<!--CODE{}-->'.format(ix), "<div class=code><code>{}</code></div>".format(match))
        return text

    def python_highlight(self, text):
        text = self.code_format(text)
        for word in self.python_reserved_words:
            text = re.sub('(?<=\\W)({})(?=\\W)'.format(word), '<red-bold>\\1</red-bold>', text)
        text = re.sub('(?<=\\W)(\\w+)(?=\\()', '<blue>\\1</blue>', text)
        text = text.replace('  ', '&nbsp;&nbsp;')
        text = text.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        return text

    def code_format(self, text):
        return text.replace('\n', '<br>\n')


class CustomImprovedMarkdown:
	pass

def mk_server(
		name="static_server",
		static_url_path='',
		static_folder='',
		template_folder='',
	    ROOT=os.path.realpath("."),
    	KEY=None,
    	analytics_path="log.txt"
	):
	app = flask.Flask(name, 
		static_url_path=static_url_path,
		template_folder=template_folder,
		static_folder=static_folder)
	if KEY is not None:
		app.secret_key = open(KEY).read()
	else:
		app.secret_key = "not_secret_at_all"
	aserv = AnalyticsSaver(analytics_path, 120)
	md = CustomMarkdown()
	yamd = CustomImprovedMarkdown()
	
	@app.before_request
	def add_to_analytics():
	    aserv.append([flask.request.remote_addr, flask.request.path])
	
	@app.route("/")
	def main():
	    return markdown_resource("index")
	
	@app.route("/file/<filename>")
	def serve_file(filename):
	    return flask.send_from_directory('file', filename)

	@app.route("/<page>.yamd")
	def markdown_resource(page):
	    with open(page + ".yamd") as f:
	        content = f.read()
	    content = yamd.convert(content)
	    return flask.render_template('root.html', content=content)
	
	@app.route("/<page>.md")
	def markdown_resource(page):
	    with open(page + ".md") as f:
	        content = f.read()
	    content = md.convert(content)
	    return flask.render_template('root.html', content=content)
	
	@app.route("/<page>.html")
	def html_resource(page):
	    with open(page + ".html") as f:
	        content = f.read()
	    return flask.render_template('root.html', content=content)

	return app
		

if __name__ == '__main__':
	app = mk_server()
	app.run('0.0.0.0', 5000)
