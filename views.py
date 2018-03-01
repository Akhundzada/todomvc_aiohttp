from aiohttp import web
from .models import Task

async def index(request):
    return web.Response(text='Hello world')


async def create_task(request):
    return True


async def edit_task(request):
    return True


async def delete_task(request):
    return True


async def complete_task(request):
    try:
        Task.complete(Task, task_id=request.GET['task_id'])
    except ValueError:
        return {'code': 404, 'message': 'Task does not exists'}