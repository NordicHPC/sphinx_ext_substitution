import os
from os.path import join as pjoin
import re

import pytest



def doc(build="_build-default", subs='-D substitute_path=substitutions/one-yaml/', opts=""):
    """Generic function to build a document with different modes"""
    assert not os.system('rm -rf testdata/proj/%s/'%build)
    assert not os.system('cd testdata/ ; sphinx-build -M html proj/ proj/%s/ -v %s %s'%(build, subs, opts))
    data = open(pjoin('testdata/proj/', build, 'html', 'index.html')).read()
    return data

@pytest.fixture(scope='session')
def doc1_default():
    """Default (replacement) version of document"""
    return doc()

@pytest.fixture(scope='session')
def doc1_both():
    """Document with substitute_mode=both"""
    return doc(build='_build-both', opts="-D substitute_mode=both")

@pytest.fixture(scope='session')
def doc1_original():
    """Document with substitute_mode=original"""
    return doc(build='_build-original', opts="-D substitute_mode=original")



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



@pytest.fixture(scope='session')
def doc1_default_rstsubs():
    """Same, but loading subs from yaml"""
    return doc(subs='-D substitute_path=substitutions/individual/')

def test_load_rstsubs(doc1_default_rstsubs):
    """Test loading from the *.rst files"""
    test_role(doc1_default_rstsubs)
    test_directive(doc1_default_rstsubs)

@pytest.fixture(scope='session')
def doc1_default_mix():
    """Same, but loading subs from both yaml and single files"""
    return doc(build='_build-mix', subs='-D substitute_path=substitutions/mix/individual/:substitutions/mix/one-yaml/')
def test_load_mix(doc1_default_mix):
    """Test loading from the *.rst files"""
    test_role(doc1_default_mix)
    test_directive(doc1_default_mix)

@pytest.fixture(scope='session')
def doc1_default_precedence_yamlfirst():
    """Same, but loading subs from both yaml and single files"""
    return doc(build='_build-precedence-yamlfirst',subs='-D substitute_path=substitutions/precedence-yamlfirst/one-yaml/:substitutions/precedence-yamlfirst/individual/')
def test_load_precedence_yamlfirst(doc1_default_precedence_yamlfirst):
    """Test loading from the *.rst files"""
    test_role(doc1_default_precedence_yamlfirst)
    test_directive(doc1_default_precedence_yamlfirst)

@pytest.fixture(scope='session')
def doc1_default_precedence_rstfirst():
    """Same, but loading subs from both yaml and single files"""
    return doc(build='_build-precedence-rstfirst', subs='-D substitute_path=substitutions/precedence-rstfirst/individual/:substitutions/precedence-rstfirst/one-yaml/')
def test_load_precedence_rstfirst(doc1_default_precedence_rstfirst):
    """Test loading from the *.rst files"""
    test_role(doc1_default_precedence_rstfirst)
    test_directive(doc1_default_precedence_rstfirst)

@pytest.fixture(scope='session')
def doc1_path_envvar():
    """Same, but loading subs from both yaml and single files"""
    try:
        os.environ['SPHINX_EXT_SUBSTITUTION_PATH'] = 'substitutions/one-yaml'
        data = doc(build='_build-path_envvar', subs='')
    finally:
        del os.environ['SPHINX_EXT_SUBSTITUTION_PATH']
    return data

def test_path_envvar(doc1_path_envvar):
    """Test loading from the *.rst files"""
    test_role(doc1_path_envvar)
    test_directive(doc1_path_envvar)
