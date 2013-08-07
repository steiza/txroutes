import routes
from twisted.web.resource import Resource


class Dispatcher(Resource):
    '''
    Provides routes-like dispatching for twisted.web.server.

    Frequently, it's much easier to describe your website layout using routes
    instead of Resource from twisted.web.resource. This small library lets you
    dispatch with routes in your twisted.web application.

    Usage:

        from twisted.internet import reactor, task
        from twisted.web.server import Site, NOT_DONE_YET

        from txroutes import Dispatcher


        # Create a Controller
        class Controller(object):

            def index(self, request):
                return '<html><body>Hello World!</body></html>'

            def docs(self, request, item):
                return '<html><body>Docs for %s</body></html>' % item.encode('utf8')

            def post_data(self, request):
                return '<html><body>OK</body></html>'

            def deferred_example(self, request):
                request.write('<html><body>Wait a tic...</body></html>')
                task.deferLater(reactor, 5, lambda: request.finish())

                return NOT_DONE_YET

        c = Controller()

        dispatcher = Dispatcher()

        dispatcher.connect(name='index', route='/', controller=c, action='index')

        dispatcher.connect(name='docs', route='/docs/{item}', controller=c,
                action='docs')

        dispatcher.connect(name='data', route='/data', controller=c,
                action='post_data', conditions=dict(method=['POST']))

        dispatcher.connect(name='deferred_example', route='/wait', controller=c,
                action='deferred_example')

        factory = Site(dispatcher)
        reactor.listenTCP(8000, factory)
        reactor.run()

    Helpful background information:
    - Python routes: http://routes.groovie.org/
    - Using twisted.web.resources: http://twistedmatrix.com/documents/current/web/howto/web-in-60/dynamic-dispatch.html
    '''

    def __init__(self):
        Resource.__init__(self)

        self.__controllers = {}
        self.__mapper = routes.Mapper()

    def connect(self, name, route, controller, **kwargs):
        self.__controllers[name] = controller
        self.__mapper.connect(name, route, controller=name, **kwargs)

    def getChild(self, name, request):
        return self

    def render(self, request):

        wsgi_environ = {}
        wsgi_environ['REQUEST_METHOD'] = request.method
        wsgi_environ['PATH_INFO'] = request.path

        result = self.__mapper.match(environ=wsgi_environ)

        handler = None

        if result is not None:
            controller = result.get('controller', None)
            controller = self.__controllers.get(controller)

            if controller is not None:
                del result['controller']
                action = result.get('action', None)

                if action is not None:
                    del result['action']
                    handler = getattr(controller, action, None)

        if handler:
            return handler(request, **result)
        else:
            request.setResponseCode(404)
            return '<html><head><title>404 Not Found</title></head>' \
                    '<body><h1>Not found</h1></body></html>'


if __name__ == '__main__':
    import logging

    import twisted.python.log
    from twisted.internet import reactor, task
    from twisted.web.server import Site, NOT_DONE_YET

    # Set up logging
    log = logging.getLogger('twisted_routes')
    log.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(handler)

    observer = twisted.python.log.PythonLoggingObserver(loggerName='twisted_routes')
    observer.start()

    # Create a Controller
    class Controller(object):

        def index(self, request):
            return '<html><body>Hello World!</body></html>'

        def docs(self, request, item):
            return '<html><body>Docs for %s</body></html>' % item.encode('utf8')

        def post_data(self, request):
            return '<html><body>OK</body></html>'

        def deferred_example(self, request):
            request.write('<html><body>Wait a tic...</body></html>')
            task.deferLater(reactor, 5, lambda: request.finish())

            return NOT_DONE_YET

    c = Controller()

    dispatcher = Dispatcher()

    dispatcher.connect(name='index', route='/', controller=c, action='index')

    dispatcher.connect(name='docs', route='/docs/{item}', controller=c,
            action='docs')

    dispatcher.connect(name='data', route='/data', controller=c,
            action='post_data', conditions=dict(method=['POST']))

    dispatcher.connect(name='deferred_example', route='/wait', controller=c,
            action='deferred_example')

    factory = Site(dispatcher)
    reactor.listenTCP(8000, factory)
    reactor.run()
