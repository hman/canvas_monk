from os import path
from werkzeug import SharedDataMiddleware
from werkzeug import Request, ClosingIterator
from werkzeug.exceptions import HTTPException

import views
from utils import local, local_manager, url_map, root_path

STATIC_PATH = path.join(root_path, 'static')

class Application(object):
    def __init__(self):
        local.application = self
        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/static': STATIC_PATH
        })

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response))
