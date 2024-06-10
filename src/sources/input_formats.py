from .source import Source

from email import policy
from email.parser import BytesParser


def open_source(filename):
    if filename.endswith('.eml'):
        cls = EmlFile
    else:
        cls = TextFile
    return cls(filename)


class TextFile(Source):

    def read_source(self):
        with open(self.path) as infile:
            for line in infile:
                yield from line.split()
                yield ""


class EmlFile(Source):

    def read_source(self):
        with open(self.path, 'rb') as infile:
            msg = BytesParser(policy=policy.default).parse(infile)

        def read_msg_part(part):
            if part.get_content_type() in ['multipart/related', 'multipart/mixed']:
                for subpart in part.iter_parts():
                    if subpart.get_content_maintype() in ('multipart', 'text'):
                        yield from read_msg_part(subpart)
            elif part.get_content_type() == 'multipart/alternative':
                subparts = list(part.iter_parts())
                types = [subpart.get_content_type() for subpart in subparts]
                for preferred_type in ('text/plain', 'text/html'):
                    if preferred_type in types:
                        yield from read_msg_part(subparts[types.index(preferred_type)])
                        break
            else:
                yield from part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8").split()

        yield from read_msg_part(msg)
