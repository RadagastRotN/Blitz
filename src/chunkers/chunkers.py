from abc import ABC


class Chunker(ABC):

    def __init__(self, source, *args, **kwargs):
        self.source = source
        self.chunks = []

    def get_chunk(self, ind):
        return " ".join(self.chunks[ind])

    def get_average_len(self):
        if self.words_count and self.chunks:
            return self.words_count / len(self.chunks)
        else:
            return 1

    def sanitize(self):
        for ind, chunk in enumerate(self.chunks):
            if len(chunk) > 30:
                self.chunks[ind] = "{}...{}".format(chunk[:6], chunk[-6:])


class BasicChunker(Chunker):

    def __init__(self, source, size=2):
        super().__init__(source)
        self.size = size
        chunk = []
        for token in self.source.tokens:
            chunk += [token]
            if len(chunk) == self.size or chunk[-1][-1] in '.?!':
                self.chunks += [chunk]
                chunk = []
        if chunk:
            self.chunks += [chunk]

        self.words_count = source.words_count
        if not self.chunks:
            self.chunks = ["<this file is empty>"]
