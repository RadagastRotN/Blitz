from abc import ABC


class Source(ABC):

    def __init__(self, path):
        self.tokens = self.read_source(path)
        self.words_count = len(self.tokens)
        self.sanitize()

    def get_chunk(self, ind):
        return " ".join(self.tokens[ind])

    def get_average_len(self):
        if self.words_count and self.tokens:
            return self.words_count / len(self.tokens)
        else:
            return 1

    def sanitize(self):
        for ind, token in enumerate(self.tokens):
            if len(token) > 30:
                self.tokens[ind] = "{}...{}".format(token[:6], token[-6:])
