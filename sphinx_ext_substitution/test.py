import os
from os.path import join as pjoin
import re

import pytest



def doc(build="_build-default", opts=""):
    """Generic function to build a document with different modes"""
    assert not os.system('rm -rf testdata/proj/%s/'%build)
    assert not os.system('cd testdata/ ; sphinx-build -M html proj/ proj/%s/ -v %s'%(build, opts))
    data = open(pjoin('testdata/proj/', build, 'html', 'index.html')).read()
    return data

@pytest.fixture(scope='session')
def doc1_default():
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



def test_role(doc1_default):
    assert "A0-original" in doc1_default

    assert "A1-id" not in doc1_default
    assert "A1-original" in doc1_default
    assert "A1-substitute" not in doc1_default

    assert "A2-id" not in doc1_default
    assert "A2-original" not in doc1_default
    assert "A2-substitute" in doc1_default

def test_role_inline_markup(doc1_default):
    assert "A3-A3" not in doc1_default
    assert "<em>A3-original</em>" in doc1_default

    assert "<em>A4-substitute</em>" in doc1_default


def test_directive(doc1_default):
    assert 'A10-id' not in doc1_default
    assert 'A10.1-original' in doc1_default
    assert '<em>A10.2-original</em>' in doc1_default

    assert 'A11.1-original' not in doc1_default
    assert '<em>A11.2-original</em>' not in doc1_default
    assert 'A11.1-substitute' in doc1_default
    assert '<em>A11.2-substitute</em>' in doc1_default


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

def test_both_css_roles(doc1_both):
    assert re.search('class="substitute-original"[^>]*>\(NO_ID\)', doc1_both)
    assert re.search('<strong class="substitute-original"[^>]*>\(A1-id\) A1-original', doc1_both)
    assert re.search('class="substitute-original"[^>]*>\(A2-id\) A2-original', doc1_both)
    assert re.search('class="substitute-replacement"[^>]*>A2-substitute', doc1_both)
    # This test combines <em> in the original and CSS, which is probably not needed:
    assert re.search('class="substitute-original"[^>]*>\(A3-id\) ?<em>A3-original', doc1_both)


def test_mode_original(doc1_original):
    assert 'A2-original' in doc1_original
    assert 'A2-substitute' not in doc1_original

    assert 'A10.1-original' in doc1_original
    assert 'A11.1-original' in doc1_original
    assert 'A11.2-substitute' not in doc1_original

def test_original_inline_markup(doc1_original):
    assert '<em>A4-original</em>' in doc1_original

    assert '<em>A10.2-original</em>' in doc1_original
    assert '<em>A11.2-original</em>' in doc1_original
