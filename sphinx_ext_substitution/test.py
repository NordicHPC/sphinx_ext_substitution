import os
from os.path import join as pjoin
#os.environ['PYTHONPATH'] = os.getcwd()


def test1():
    assert not os.system('cd testdata/proj ; make clean html')

    data = open(pjoin('testdata/proj', '_build', 'html', 'index.html')).read()

    assert "original-A0" in data

    assert "id-A1" not in data
    assert "original-A1" in data
    assert "substitute-A1" not in data

    assert "id-A2" not in data
    assert "original-A2" not in data
    assert "substitute-A2" in data
