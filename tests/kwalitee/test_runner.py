import os
import shutil
import tempfile
import pytest

from cheesecake_kwalitee_index.kwalitee import runner


@pytest.fixture
def temp_dir(request):
    d = tempfile.mkdtemp(prefix='cheesecake_')
    
    def finalizer():
        shutil.rmtree(d)

    request.addfinalizer(finalizer)
    return d


class TestDownload:
    def test_basic_download(self, temp_dir):
        package = 'requests'
        assert os.listdir(temp_dir) == []
        runner.download(package, temp_dir)
        assert os.listdir(temp_dir) != []

    def test_invalid_package(self, temp_dir):
        package = 'asdswdversbvfr'
        assert os.listdir(temp_dir) == []
        ret = runner.download(package, temp_dir)
        assert os.listdir(temp_dir) == []
        assert ret != 0

    def test_with_version(self, temp_dir):
        package = 'requests~=2.10.0'
        assert os.listdir(temp_dir) == []
        runner.download(package, temp_dir)
        assert os.listdir(temp_dir) != []
        

class TestLint:
    def test_basic(self, temp_dir):
        # We need to specify the exact version for a small package 
        # In this case, we know version 0.1.5 of auto-changelog gets
        # 3.60 out of 10
        name = 'auto-changelog'
        version = '0.1.5'
        runner.download(name + '==' + version, temp_dir)
        score = runner.lint(temp_dir, name.replace('-', '_'))
        assert str(score) == '3.6'
