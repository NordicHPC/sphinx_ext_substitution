import os
from os.path import join as pjoin
#os.environ['PYTHONPATH'] = os.getcwd()

import pytest

@pytest.fixture(scope='session')
def doc1():
    assert not os.system('cd testdata/proj ; make clean html')
    data = open(pjoin('testdata/proj', '_build', 'html', 'index.html')).read()
    return data

def test_role(doc1):

    assert "A0-original" in doc1

    assert "A1-id" not in doc1
    assert "A1-original" in doc1
    assert "A1-substitute" not in doc1

    assert "A2-id" not in doc1
    assert "A2-original" not in doc1
    assert "A2-substitute" in doc1

def test_role_inline_markup(doc1):

    assert "A3-A3" not in doc1
    assert "<em>A3-original</em>" in doc1

    assert "<em>A4-substitute</em>" in doc1


def test_directive(doc1):
    assert 'A10-id' not in doc1
    assert 'A10.1-original' in doc1
    assert '<em>A10.2-original</em>' in doc1

    #assert 'A11.1-original' not in doc1
    #assert '<em>A11.2-original</em>' not in doc1
    #assert 'A11.1-substitute' not in doc1
    #assert '<em>A11.1-substitute</em>' in doc1

