from sqlalchemy.orm import Session
from models import engine
from models import Users, Multimedia, Posts
import logging
import sys
from logging import StreamHandler, Formatter

from .ml_models import SuicidalSignalModel
from .ml_models import SentimentModel

session = Session(bind=engine)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

config # = 

MODELS = {
    "suicidal_signal": SuicidalSignalModel(config),
    "sentiment": SentimentModel()
}

def get_new_user_posts(user_id: int):
    posts = session.query(Posts).where(Posts.user_id == id and Posts.annotation == -1).all()
    for attr_model, model in MODELS.items():
        labels = model.predict(posts)
        
    for p in posts:
        p.annotation #=  