import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task:
    @staticmethod
    def possible_routes():
        return
        {
            'GET': {'/': 'index', '/view': 'view'},
            'POST': {
                        '/create': 'create', '/edit': 'edit',
                        '/complete': 'complete',
                     }
        }

    engine = create_engine('sqlite:///todomvc.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)

    __tablename__ = 'task'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    completed = sa.Column(sa.Boolean, nullable=False, default=False)

    def complete(self, task_id):
        task = session.query(Task).get(task_id)
        session.query(Task).update({'completed': not task.completed})

    def create(self, data):
        session.query(self).create(data)

    def edit(self, data):
        task = session.query(self).get(data.id)
        session.query(self).update(data)


engine = create_engine('sqlite:///todomvc.sqlite')
session = sessionmaker()
session.configure(bind=engine)

Base.metadata.create_all(engine)



