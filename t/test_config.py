from lazyscripts.config import Config
from t import get_datadir

def test_load_config():
  conf = Config(get_datadir()+'repository.conf')
  print conf.default_repo
  assert conf.default_repo == 'git://a.b.c', conf.defualt_repo
