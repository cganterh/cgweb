# -*- coding: UTF-8 -*-

from os.path import join as joinpath
import codecs
from tornado import ioloop
from tornado.web import Application, RequestHandler
from markdown import markdown

md_dir = './markdown'

class BaseHandler(RequestHandler):
    def render(self, template_name, **kwargs):
        #en vez de esto deberia de ocupar: RequestHandler.static_url(path, include_host=None, **kwargs)
        RequestHandler.render(self, template_name,
                              host=self.request.host, **kwargs)

class MDHandler(BaseHandler):
    def get(self, *args):
        self.render('base.html',
                    content=self.get_md(args[0]))
            
    def get_md(self, md_file):
        path = joinpath(md_dir, md_file)
        with codecs.open(path, encoding='utf-8') as f:
            return markdown(f.read())

class HomeHandler(MDHandler):
    def get(self):
        self.render('home.html',
                    about=self.get_md('about.md'),
                    ramos=self.get_md('ramos.md'))

application = Application(
    [('/$', HomeHandler),
     ('/(.*\.md)', MDHandler)],
    debug = False,
    static_path = './static',
    static_url_prefix = '/static/',
    template_path = './templates',
)

if __name__ == "__main__":
    application.listen(8888)
    ioloop.IOLoop.instance().start()
