import itertools

import requests


class Word(object):
    def __init__(self, value):
        self.value = value
        self.similar_words = self.get_similar_words()

    def get_similar_words(self):
        url = "https://api.datamuse.com/words?sp=" + self.value
        similar = {word_dic['word'] for word_dic in requests.get(url).json() if word_dic['score'] > 90}

        url = "https://api.datamuse.com/words?sl=" + self.value
        sound_like = {word_dic['word'] for word_dic in requests.get(url).json() if word_dic['score'] > 90}

        suggestions = similar.union(sound_like)

        if self.value.startswith("py"):
            suggestions.add(self.value[2:])
        else:
            suggestions.add("py" + self.value)

        suggestions.add(''.join(ch for ch, _ in itertools.groupby(self.value)))

        try:
            suggestions.remove(self.value)
        except:
            pass
        return suggestions