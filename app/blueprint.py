from flask import Blueprint
from flask import render_template




simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/')
def home():
    return render_template('index.html')


@simple_page.route("/test_celery")
def index_view():
    return "Flask-celery task scheduler!"


# @simple_page.route("/timer")
# def timer_view():
#     time_counter = redis_db.mget(["minute", "second"])
#     return f"Minute: {time_counter[0]}, Second: {time_counter[1]}"


