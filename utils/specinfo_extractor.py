from nltk import word_tokenize

import pymorphy2
import re
import pandas as pd

class SpecInfoExtractor:
    def __init__(self, config):
        self.regex = []
        for tag, regex in config["regex"]:
            self.regex.append( (tag, re.compile(regex)))
        towns = pd.read_csv(config["russian_town_list"], sep="|")
        towns = towns[0].to_list()

        self.towns = self._extend_towns(towns, config["town_exclude_list"])

        with open(config["russian_names"]) as f:
            self.names = f.read().lower().split()

    def _extend_towns(self, towns: list, town_exclude_list):
        morph = pymorphy2.MorphAnalyzer()
        towns_extended = []
        for t in towns:
            for form in ["gent", "loct"]:
                town = morph.parse(t.lower())[0]
                try:
                    town = town.inflect({form}).word
                except:
                    continue
                towns_extended.append(town)

        for i in town_exclude_list:
            towns_extended.pop(towns_extended.index(i)) 
        return towns_extended

    def extract_data(self, texts:list):
        messages = []
        for m in texts:
            tokenized = word_tokenize(m.lower())
            for name in self.names:
                if name in tokenized:
                    messages.append("[NAME] " + m)
            for name, r in self.regex:
                if r.search(m) != None:
                    messages.append(f"{name} " + m)
            for t in self.towns_extended:
                if t in tokenized:
                    messages.append("[TOWN] " + m)
        return messages
