import views


def setup_routes(app):
    app.router.add_get('/', views.index)
    app.router.add_post('/create', views.create_task)
    app.router.add_post('/edit/<int:id>', views.edit_task)
    app.router.add_delete('/<int:id>', views.delete_task)
