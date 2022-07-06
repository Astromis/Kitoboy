from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer

import torch
import numpy as np
import re
from transformers import AutoTokenizer, AutoModel
from textfab import Conveyer
from xgboost import XGBClassifier
from typing import List

from abc import ABCMeta, abstractmethod

import logging
from logging import StreamHandler, Formatter
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

class BaseMlModel(metaclass=ABCMeta):
    
    @abstractmethod
    def predict(self, texts: List[str]):
        raise NotImplementedError
    
    @abstractmethod
    def _vectorize(self, texts: List[str]):
        raise NotImplementedError

class SentimentModel(BaseMlModel):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Sentiment model initialization")
        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)
        logger.info("Initizalization done")

    def predict(self, texts: List[str]):
        
        results = self.model.predict(texts, k=1)
        label = []

        for x, _ in list([list(x.items())[0] for x in results]):
            label.append(x)
        return label
    
    def _vectorize(self, texts: List[str]):
        pass

class SuicidalSignalModel(BaseMlModel):
    def __init__(self, config) -> None:
        super().__init__()
        logger.info("BERT model initialization")
        self.bert_tokenizer = AutoTokenizer.from_pretrained(config['bert_model'])
        self.bert_model = AutoModel.from_pretrained(config['bert_model'])
        self.model = self.model.to(config["device"])
        logger.info("Initialization done")
        logger.info("Suicidal model initialization")
        self.clf = XGBClassifier()
        self.clf.load_model(config['suicidal_signals_model_path'])
        self.text_preprocessor = Conveyer(config["conveyer_config"])
        logger.info("Initialization done")
        self.batch_size = config["batch_size"]

    def _vectorize(self, texts: List[str]):
        texts_len = len(texts)
        batch_size = self.batch_size

        vectors = []
        for i in range(0, texts_len, batch_size):
            if i+batch_size > texts_len:
                batch_size = texts_len % batch_size
            text_block = texts[i:i+batch_size] 
            t = self.tokenizer(text_block, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
            embeddings = model_output.last_hidden_state[:, 0, :]
            embeddings = torch.nn.functional.normalize(embeddings)
            vectors.append(embeddings[0].cpu().numpy())
        
        vectors = np.vstack(vectors)
        assert vectors.shape[0] == texts_len
        return np.vstack(vectors)

    def _preprocess_text(self, text):
        text = list(map(lambda x: re.sub(r"<emoji>.+</emoji>", "", x), text))
        text = list(filter(lambda x: "<no text>" not in x, text))
        text = list(map(lambda x:re.sub("[A-Za-z]+", '', x), text))
        text = self.text_preprocessor.start(text)
        text = list(filter(lambda x: len(x) > 2, text))
        return text

    def predict(self, texts: List[str]):
        processed_texts = self._preprocess_text(texts)
        vectors = self._vectorize(processed_texts)
        return self.clf.predict(vectors).tolist()




