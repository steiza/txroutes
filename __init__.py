import routes
from twisted.web.resource import Resource


class Dispatcher(Resource):
    '''
    Provides routes-like dispatching for twisted.web.server.

    Frequently, it's much easier to describe your website layout using routes
    instead of Resource from twisted.web.resource. This small library lets you
    dispatch with routes in your twisted.web application.


    Usage:

        from twisted.internet import reactor
        from twisted.web.server import Site

        # Create a Controller
        class Controller(object):

            def index(self, request):
                return '<html><body>Hello World!</body></html>'

            def docs(self, request):
                return '<html><body>Docs!</body></html>'

        c = Controller()

        dispatcher = Dispatcher()
        dispatcher.connect(name='index', route='/', controller=c, action='index')
        dispatcher.connect(name='docs', route='/docs/{item}', controller=c,
                action='docs')

        factory = Site(dispatcher)
        reactor.listenTCP(8000, factory)
        reactor.run()


    Helpful background information:
    - Python routes: http://routes.groovie.org/
    - Using twisted.web.resources: http://twistedmatrix.com/documents/current/web/howto/web-in-60/dynamic-dispatch.html


    Todo:
    - Support dispatching based on HTTP verbs (GET, POST, etc.)
    - Support wildcard routes variables getting passed into contoller's handlers
    '''

    def __init__(self):
        Resource.__init__(self)

        self.__path = ['']

        self.__controllers = {}
        self.__mapper = routes.Mapper()

    def connect(self, name, route, controller, **kwargs):
        self.__controllers[name] = controller
        self.__mapper.connect(name, route, controller=name, **kwargs)

    def getChild(self, name, request):
        self.__path.append(name)
        return self

    def render(self, request):
        try:
            result = self.__mapper.match('/'.join(self.__path))

            handler = None

            if result is not None:
                controller = result.get('controller', None)
                controller = self.__controllers.get(controller)

                if controller is not None:
                    action = result.get('action', None)

                    if action is not None:
                        handler = getattr(controller, action, None)

        finally:
            self.__path = ['']

        if handler:
            return handler(request)
        else:
            request.setResponseCode(404)
            return '<html><head><title>404 Not Found</title></head>' \
                    '<body><h1>Not found</h1></body></html>'


if __name__ == '__main__':
    import logging

    import twisted.python.log
    from twisted.internet import reactor
    from twisted.web.server import Site

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

        def docs(self, request):
            return '<html><body>Docs!</body></html>'

    c = Controller()

    dispatcher = Dispatcher()
    dispatcher.connect(name='index', route='/', controller=c, action='index')
    dispatcher.connect(name='docs', route='/docs/{item}', controller=c,
            action='docs')

    factory = Site(dispatcher)
    reactor.listenTCP(8000, factory)
    reactor.run()
