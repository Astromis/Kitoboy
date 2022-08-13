from flask import Blueprint
from flask import render_template
from .models import DigitalUsers, DuserRisk, Posts

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/')
def home():
    users = DigitalUsers.get_all()
    print(users[0].suicide_rating)
    return render_template('index.html', user_list=users)

@simple_page.route("/<user_id>/posts/")
def view_user_post(user_id):
    posts = Posts.get_list(user_id=user_id)
    return render_template("view_posts.html", posts=posts)