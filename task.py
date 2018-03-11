from db import table_todo_list
from aiohttp import web
from sqlalchemy import sql

def required_keys():
    return ['name', 'is_completed']

async def get_tasks(request):
    async with request.app['db'].acquire() as connection:
        tasks = [
            dict(row.items()) async
            for row in connection.execute(
                table_todo_list.select().order_by(table_todo_list.id)
            )
        ]
    return web.json_response({'code': 200, 'body': tasks})


async def get_single(request):
    id = int(request.match_info['id'])
    async with request.app['db'].acquire() as connection:
        result = await connection.execute(
            table_todo_list.select().where(table_todo_list.id == id)
        )
    row = await result.fetchone()

    if not row:
        return web.json_response({'code': 404, 'body': 'Task not found'})

    return web.json_response({'code': 200, 'body': dict(row.items())})


async def remove(request):
    id = int(request.match_info['id'])

    async with request.app['db'].acquire() as connection:
        result = await connection.execute(
            table_todo_list.delete().where(table_todo_list.id == id)
        )

    if not result.rowcount:
        return web.json_response({'code': 404, 'body': 'Task not found'})

    return web.json_response({'code': 200, 'body': 'OK'})


async def update(request):
    id = int(request.match_info['id'])
    data = await request.json()

    for key in required_keys():
        if key not in data:
            return web.json_response({'code': 400,
                                      'body': key + ' is required'})

    todo = {'name': data['name'], 'is_completed': bool(data['is_completed'])}

    async with request.app['db'].acquire() as connection:
        result = await connection.execute(
            table_todo_list.update().where(
                table_todo_list.id == id).values(todo)
        )

    if result.rowcount == 0:
        return web.json_response({'code': 404, 'body': 'Task not found'})

    return web.json_response({'code': 200, 'body': 'OK'})


async def create(request):
    id = int(request.match_info['id'])
    data = await request.json()

    for key in required_keys():
        if key not in data:
            return web.json_response({'code': 400,
                                      'body': key + ' is required'})

    todo = {'name': data['name'], 'is_completed': bool(data['is_completed'])}

    async with request.app['db'].acquire() as connection:
        await connection.execute(
            table_todo_list.insert().values(todo)
        )

        result = await connection.execute(
            sql.select([sql.func.max(table_todo_list.c.id).label('id')])
        )
        return_id = await result.fetchone()

    return web.json_response(
        {'code': 200, 'body': {'id': return_id}}
    )
