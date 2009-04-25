from lazyscripts import repo
from lazyscripts.info import get_distro

def test_get_repo_from_distro():
    _repo = repo.get_repo_for_distro(get_distro(), True)
    assert 'Repo' == _repo.__class__.__name__, _repo
