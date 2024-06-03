from .chunker import Chunker

from email import policy
from email.parser import BytesParser


class TextFile(Chunker):

    def read_source(self, filename):
        with open(filename) as infile:
            return sum((line.split() for line in infile), [])


class EmlFile(Chunker):
    def read_source(self, filename):
        with open(filename, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        text = []

        # Get the email body
        if msg.is_multipart():
            for part in msg.walk():
                # Get the plain text part
                if part.get_content_type() in ['text/plain', 'text/html']:
                    text += [part.get_payload(decode=True).decode(part.get_content_charset())]
        else:
            # If the email is not multipart, just get the payload
            text = [msg.get_payload(decode=True).decode(msg.get_content_charset())]

        return sum((line.split() for line in text), [])
