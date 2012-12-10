txroutes
========

txroutes provides routes-like dispatching for twisted.web.server (it actually
depends upon the Python routes codebase).

Frequently, it's much easier to describe your website layout using routes
instead of Resource from twisted.web.resource. This small library lets you
dispatch with routes in your twisted.web application.

Usage
-----

Here is an example of how to use txroutes::

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

License
-------
txroutes is released under the `MIT License`__

__ http://opensource.org/licenses/MIT

Additional Information
----------------------
- Python routes: http://routes.groovie.org/
- Using twisted.web.resources: http://twistedmatrix.com/documents/current/web/howto/web-in-60/dynamic-dispatch.html
