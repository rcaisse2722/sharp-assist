import urllib.request
import abc

# Base interface
class IHtmlProvider(abc.ABC):

    @abc.abstractmethod
    def __init__(self, path):
        pass

    @abc.abstractmethod
    def get_html(self):
        pass

# Web request implementation of IHtmlProvider
class UrlHtmlProvider(IHtmlProvider):

    def __init__(self, path):
        self.path = path

    def get_html(self):
        return urllib.request.urlopen(self.path)
        
# File implementation of IHtmlProvider
class FileHtmlProvider(IHtmlProvider):

    def __init__(self, path):
        self.path = path

    def get_html(self):
        with open(self.path, 'r', errors="surrogateescape") as testFile:
            doc = testFile.read()
        return doc.encode('utf-8', 'surrogateescape').decode('ISO-8859-1')