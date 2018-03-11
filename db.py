from aiomysql.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()
table_todo_list = sa.Table(
    'todo_list', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), unique=True, nullable=False),
    sa.Column('is_completed', sa.Boolean(), default=False, nullable=False)
)


async def create_table(engine):
    async with engine.acquire() as connection:
        await connection.execute('DROP TABLE IF EXISTS `todo_list`')
        await connection.execute('''
        CREATE TABLE `todo_list` (
        `id` INTEGER(11) AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL UNIQUE,
        `is_completed` BOOLEAN NOT NULL DEFAULT FALSE)
        ''')


async def on_start(app):
    app['db'] = await create_engine(
        ' '.join(
            [
                'host=localhost',
                'port=3306',
                'dbname=todo',
                'username=root',
                'password=!81+jaCyyILCUPg',
            ]
        )
    )


async def on_destruct(app):
    app['db'].close()
    await app['db'].wait_closed()
    app['db'] = None


async def initial_tasks(engine):
    async with engine.acquire() as connection:
        await connection.execute(table_todo_list.insert().values(
            {'name': 'First todo', 'is_completed': False}))

        await connection.execute(table_todo_list.insert().values(
            {'name': 'Second todo', 'is_completed': False}
        ))


async def setup_db(app):
    await create_table(app['db'])
    await initial_tasks(app['db'])