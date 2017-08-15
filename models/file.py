

class SparkFile(object):

    def __init__(self, session, url):
        self._session = session
        self._url = url
        print(url)
        self._filename = None

    @property
    def url(self):
        return self._url

    @property
    def filename(self):
        if not self._filename:
            resp = resp = self._session.head(self.url)
            c_disp = resp.headers.get('Content-Disposition')
            self._filename = c_disp.split('filename=')[1].replace('"', '')
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val
        return

    def download(self, path='./'):
        resp = self._session.get(self.url, stream=True)
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
