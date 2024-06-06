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

        # Get the email body
        if msg.is_multipart():
            for part in msg.walk():
                # Get the plain text part
                if part.get_content_type() in ['text/plain', 'text/html']:
                    yield from part.get_payload(decode=True).decode(part.get_content_charset()).split()
        else:
            # If the email is not multipart, just get the payload
            yield from msg.get_payload(decode=True).decode(msg.get_content_charset()).split()
