from .chunker import Chunker


class BasicChunker(Chunker):

    def __init__(self, source, size=2):
        self.source = source
        self.size = size
        self.chunks = []
        chunk = []
        for token in self.source.chunks:
            chunk += [token]
            if len(chunk) == self.size or chunk[-1][-1] in '.?!':
                self.chunks += [chunk]
                chunk = []
        if chunk:
            self.chunks += [chunk]

        self.words_count = source.words_count
