from app.app import app, manager, celery_instance
from app.blueprint import simple_page


app.register_blueprint(simple_page)



@manager.command
def runserver():
    celery_instance.start()
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    manager.runserver()
