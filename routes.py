from views import *
from .models import Task

def setup_routes(app):
    for method, route in Task.possible_routes():
        if route.length > 0:
            for r in route:
                if (method == 'GET'):
                    app.router.add_get (r, )

    app.router.add_get('/', index)