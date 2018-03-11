from aiohttp import web
import db
import task
from sys import argv


def app_factory(args=()):
    app = web.Application()

    app.on_startup.append(db.on_start(app))
    app.on_teardown.append(db.on_destruct(app))

    if '--create-table' in argv:
        app.on_startup.append(db.setup_db())

    app.router.add_get('/task/', task.get_tasks, name='get_tasks')
    app.router.add_post('/task/', task.create, name='create_task')
    app.router.add_get('/task/{id:\d+}', task.get_single, name='single_task')
    app.router.add_put('/task/{id:\d+}', task.update, name='update_task')
    app.router.add_delete('/task/{id:\d+}', task.remove, name='remove_task')

    return app