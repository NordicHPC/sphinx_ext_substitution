import os
from os.path import join as pjoin
#os.environ['PYTHONPATH'] = os.getcwd()

import pytest

@pytest.fixture(scope='session')
def doc1():
    assert not os.system('cd testdata/proj ; make clean html')
    data = open(pjoin('testdata/proj', '_build', 'html', 'index.html')).read()
    return data

def test1(doc1):

    assert "original-A0" in doc1

    assert "id-A1" not in doc1
    assert "original-A1" in doc1
    assert "substitute-A1" not in doc1

    assert "id-A2" not in doc1
    assert "original-A2" not in doc1
    assert "substitute-A2" in doc1

def test_inline_markup(doc1):

    assert "id-A3" not in doc1
    assert "<em>original-A3</em>" in doc1

    assert "<em>substitute-A4</em>" in doc1
