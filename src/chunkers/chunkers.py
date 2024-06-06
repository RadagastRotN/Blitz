from abc import ABC


class Chunker(ABC):

    def __init__(self, source, *args, **kwargs):
        self.source = source
        self.chunks = list(self.gen_chunks(*args, **kwargs))
        if not self.chunks:
            self.chunks = ["<this file is empty>"]
        self.average_len = self.source.tokens_count / len(self.chunks) if self.source.tokens_count else 1
        self.tokens_count = source.tokens_count

    def __getitem__(self, item):
        return self.chunks[item]

    def __len__(self):
        return len(self.chunks)


class BasicChunker(Chunker):

    def gen_chunks(self, size=2):
        chunk = []
        for token in self.source:
            if token:
                chunk += [token]
            if len(chunk) == size or not token or token[-1] in '.?!':
                yield " ".join(chunk)
                chunk.clear()
        if chunk:
            yield " ".join(chunk)
