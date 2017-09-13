'''
sparkpy.models.file
~~~~~~~~~~~~~~~~~~~
A class to handle files attached to a Cisco Spark Message
'''

from ..session import SparkSession
from os import sep
from os.path import expanduser

download_path = expanduser(f'~{sep}Downloads{sep}')


class SparkFile(object):
    '''
    An object representing a file attached to a Cisco Spark Message

    :param url: The url of the file
    :type url: str
    '''

    def __init__(self, url):
        self._url = url
        self._filename = None

    @property
    def url(self):
        ''' The url of the file '''
        return self._url

    @property
    def filename(self):
        ''' The filename. This is fetched when accessed or downloaded '''
        if not self._filename:
            with SparkSession() as s:
                resp = resp = s.head(self.url)
                c_disp = resp.headers.get('Content-Disposition')
                self._filename = c_disp.split('filename=')[1].replace('"', '')
            return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val
        return

    def download(self, path=download_path):
        '''
        Download the file to the specified path

        :param path: (optional) Specify a path to save the file to.
                     If the paramater is not passed then the file is saved to
                     the users download directory.
        '''
        with SparkSession() as s:
            resp = s.get(self.url, stream=True)
            if not self._filename:
                c_disp = resp.headers.get('Content-Disposition')
                if c_disp:
                    self.filename = c_disp.split('filename=')[1].replace('"', '')
                with open(path + self.filename, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

    def __repr__(self):
        return f'SparkFile({self.filename})'
