from abc import ABC


class Chunker(ABC):

    def __init__(self, path):
        self.chunks = self.read_source(path)
        self.words_count = len(self.chunks)
        self.sanitize()

    def get_chunk(self, ind):
        return " ".join(self.chunks[ind])

    def get_average_len(self):
        return self.words_count / len(self.chunks)

    def sanitize(self):
        for ind, chunk in enumerate(self.chunks):
            if len(chunk) > 30:
                self.chunks[ind] = "{}...{}".format(chunk[:6], chunk[-6:])
