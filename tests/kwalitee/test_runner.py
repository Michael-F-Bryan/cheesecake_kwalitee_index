import os
import shutil
import tempfile
import pytest

from cheesecake_kwalitee_index.kwalitee import evaluator
from cheesecake_kwalitee_index.kwalitee.models import Score


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
        evaluator.download(package, temp_dir)
        assert os.listdir(temp_dir) != []

    def test_invalid_package(self, temp_dir):
        package = 'asdswdversbvfr'
        assert os.listdir(temp_dir) == []
        ret = evaluator.download(package, temp_dir)
        assert os.listdir(temp_dir) == []
        assert ret != 0

    def test_with_version(self, temp_dir):
        package = 'requests~=2.10.0'
        assert os.listdir(temp_dir) == []
        evaluator.download(package, temp_dir)
        assert os.listdir(temp_dir) != []


class TestLint:
    def test_basic(self, temp_dir):
        # We need to specify the exact version for a small package
        # In this case, we know version 0.1.5 of auto-changelog gets
        # 3.60 out of 10
        name = 'auto-changelog'
        version = '0.1.5'
        evaluator.download(name + '==' + version, temp_dir)
        score = evaluator.lint(temp_dir, name.replace('-', '_'))
        assert str(score) == '3.6'

    def test_invalid(self, temp_dir):
        # We need to specify the exact version for a small package
        # In this case, we know version 0.1.5 of auto-changelog gets
        # 3.60 out of 10
        name = '1232ewcfswcas'
        version = '0.1.5'
        evaluator.download(name + '==' + version, temp_dir)

        with pytest.raises(RuntimeError):
            score = evaluator.lint(temp_dir, name.replace('-', '_'))


class TestVersion:
    def test_basic(self, temp_dir):
        name = 'auto-changelog'
        version = '0.1.5'
        evaluator.download(name + '==' + version, temp_dir)
        version_number = evaluator.get_version_number(temp_dir,
                name.replace('-', '_'))
        assert version_number == version


@pytest.fixture
def ev(request):
    ev = evaluator.Evaluator('auto-changelog', '0.1.5')
    request.addfinalizer(ev.clean_up)
    return ev


class TestEvaluator:
    def test_init(self, ev):
        assert ev.package == 'auto-changelog'
        assert ev.version == '0.1.5'
        assert isinstance(ev.score, dict)
        assert isinstance(ev.score['lint'], evaluator.Score)

    def test_install(self, ev):
        """
        Make sure that we can install correctly.
        """
        ret = ev.install_package()
        assert ret != 0

    def test_invalid_install(self, ev):
        """
        Make sure that installation errors are handled appropriately.
        """
        ev = evaluator.Evaluator('23twfevadsfg', '0.1.5')
        ret = ev.install_package()
        assert ret == 0

    def test_linter(self, ev):
        assert ev.install_package() != 0

        # run the linter
        lint_score = ev.lint_test()
        assert lint_score == 36

    def test_get_version(self, ev):
        version_number = ev.get_version()
        assert version_number == 10
        assert ev.version_number == '0.1.5'

    def test_evalualate_score(self, ev):
        score, total = ev.evaluate_score()

        should_be = {
            'install': Score(10, 10),
            'version_number': Score(10, 10),
            'lint': Score(36, 100),
        }
        print(ev.score)
        assert total == sum(value.total for value in ev.score.values())
        assert score == 10 + 36 + 10
        assert ev.score == should_be
