
class Config:

  def __init__(self, path=None):
      self.path = path
      self._attrs = {}

  def __getattr__(self, key):
      if not self._attrs and self.path:
        self._attrs = self._parse(open(self.path).read())

      try:
        return self._attrs[key]
      except KeyError:
        return None

  def _parse(self, content):
      tmp_arr = {}
      tmp_arr['default_repo'] = content.strip()
      return tmp_arr
