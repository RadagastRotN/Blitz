from abc import ABC, abstractmethod


class Source(ABC):

    def __init__(self, path):
        self.path = path
        self.tokens_count = sum(1 for _ in self.read_source())

    def __len__(self):
        return self.tokens_count

    def __iter__(self):
        for token in self.read_source():
            yield self.sanitize(token)

    @abstractmethod
    def read_source(self):
        pass

    @staticmethod
    def sanitize(token):
        if len(token) > 30:
            return "{}...{}".format(token[:6], token[-6:])
        else:
            return token
