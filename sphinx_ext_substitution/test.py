import os
from os.path import join as pjoin
#os.environ['PYTHONPATH'] = os.getcwd()

import pytest



def doc(build="_build-default", opts=""):
    """Generic function to build a document with different modes"""
    assert not os.system('rm -rf testdata/proj/%s/'%build)
    assert not os.system('cd testdata/ ; sphinx-build -M html proj/ proj/%s/ -v %s'%(build, opts))
    data = open(pjoin('testdata/proj/', build, 'html', 'index.html')).read()
    return data

@pytest.fixture(scope='session')
def doc1():
    """Default (replacement) version of document"""
    return doc()

@pytest.fixture(scope='session')
def doc1_both():
    """Document with substitute_mode=both"""
    return doc(build='_build-both', opts="-vv -D substitute_mode=both")

@pytest.fixture(scope='session')
def doc1_original():
    """Document with substitute_mode=original"""
    return doc(build='_build-original', opts="-vv -D substitute_mode=original")



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

    assert 'A11.1-original' not in doc1
    assert '<em>A11.2-original</em>' not in doc1
    assert 'A11.1-substitute' in doc1
    assert '<em>A11.2-substitute</em>' in doc1


def test_mode_both(doc1_both):
    assert 'A2-original' in doc1_both
    assert 'A2-substitute' in doc1_both

    assert 'A10.1-original' in doc1_both
    assert 'A11.1-original' in doc1_both
    assert 'A11.2-substitute' in doc1_both

def test_both_inline_markup(doc1_both):
    assert '<em>A4-original</em>' in doc1_both
    assert '<em>A4-substitute</em>' in doc1_both

    assert '<em>A10.2-original</em>' in doc1_both
    assert '<em>A11.2-original</em>' in doc1_both
    assert '<em>A11.2-substitute</em>' in doc1_both

def test_mode_both(doc1_original):
    assert 'A2-original' in doc1_original
    assert 'A2-substitute' not in doc1_original

    assert 'A10.1-original' in doc1_original
    assert 'A11.1-original' in doc1_original
    assert 'A11.2-substitute' not in doc1_original

def test_original_inline_markup(doc1_original):
    assert '<em>A4-original</em>' in doc1_original

    assert '<em>A10.2-original</em>' in doc1_original
    assert '<em>A11.2-original</em>' in doc1_original
