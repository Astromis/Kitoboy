from app.app import app, manager, celery_instance

from app.blueprint import simple_page

# from app.auth_api.blueprint import blueprint as auth_module
# from app.tasks_manager_api.blueprint import blueprint as tm_module
# from app.datasets.blueprint import blueprint as ds_module
# from app.storage.blueprint import blueprint as storage_module
# from app.projects_api.blueprint import blueprint as projects_module
#
app.register_blueprint(simple_page)
#
# app.register_blueprint(storage_module)
#
# app.register_blueprint(auth_module,
#                        url_prefix=app.config['URL_PREFIX_AUTH_API'])
#
# app.register_blueprint(tm_module,
#                        url_prefix=app.config['URL_PREFIX_TASK_MANAGER_API'])
#
# app.register_blueprint(projects_module,
#                        url_prefix=app.config['URL_PREFIX_TASK_MANAGER_API'])


@manager.command
def runserver():
    celery_instance.start()
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    manager.run()




#
# import os
#
# from flask import Flask, render_template
#
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
#
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)