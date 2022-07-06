from sqlalchemy.orm import Session
from models import engine
from models import Users, Multimedia, Posts
import logging
import sys
from logging import StreamHandler, Formatter

session = Session(bind=engine)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def get_new_user_posts(user_id: int):
    posts = session.query(Posts).where(Posts.user_id == id and Posts.annotation == -1).all()

    for p in posts:
        p.annotation #=  