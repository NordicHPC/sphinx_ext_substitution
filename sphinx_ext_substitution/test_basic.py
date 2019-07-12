from __future__ import print_function

import os
from os.path import join as pjoin
import re

import pytest



def doc(build="_build-default", subs='-D substitute_path=substitutions/one-yaml/', opts=""):
    """Generic function to build a document with different modes"""
    assert not os.system('rm -rf testdata/proj/%s/'%build)
    assert not os.system('cd testdata/ ; PYTHONPATH=.. sphinx-build -M html proj/ proj/%s/ -v %s %s'%(build, subs, opts))
    data = { }
    data['index'] = open(pjoin('testdata/proj/', build, 'html', 'index.html')).read()
    data['sub-list'] = open(pjoin('testdata/proj/', build, 'html', 'sub-list.html')).read()
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
    index = doc1_default['index']
    assert "A0-original" in index

    assert "A1-id" not in index
    assert "A1-original" in index
    assert "A1-substitute" not in index

    assert "A2-id" not in index
    assert "A2-original" not in index
    assert "A2-substitute" in index

def test_role_inline_markup(doc1_default):
    index = doc1_default['index']
    assert "A3-A3" not in index
    assert "<em>A3-original</em>" in index

    assert "<em>A4-substitute</em>" in index


def test_directive(doc1_default):
    index = doc1_default['index']
    assert 'A10-id' not in index
    assert 'A10.1-original' in index
    assert '<em>A10.2-original</em>' in index

    assert 'A11.1-original' not in index
    assert '<em>A11.2-original</em>' not in index
    assert 'A11.1-substitute' in index
    assert '<em>A11.2-substitute</em>' in index


def test_mode_both(doc1_both):
    index = doc1_both['index']
    assert 'A2-original' in index
    assert 'A2-substitute' in index

    assert 'A10.1-original' in index
    assert 'A11.1-original' in index
    assert 'A11.2-substitute' in index

def test_both_inline_markup(doc1_both):
    index = doc1_both['index']
    assert '<em>A4-original</em>' in index
    assert '<em>A4-substitute</em>' in index

    assert '<em>A10.2-original</em>' in index
    assert '<em>A11.2-original</em>' in index
    assert '<em>A11.2-substitute</em>' in index

def test_pre(doc1_default, doc1_both, doc1_original):
    index = doc1_default['index']
    assert 'class="pre">A7-original' in index
    assert 'class="pre">A8-substitute' in index

    index = doc1_both['index']
    assert 'class="pre">A7-original' in index
    assert 'class="pre">A8-original' in index
    assert 'class="pre">A8-substitute' in index

    index = doc1_original['index']
    assert 'class="pre">A7-original' in index
    assert 'class="pre">A8-original' in index

def test_both_css_roles(doc1_both):
    index = doc1_both['index']
    assert re.search(r'class="substitute-original"[^>]*>\(NO_ID\)', index)
    assert re.search(r'<strong class="substitute-original"[^>]*>\(A1-id\) A1-original', index)
    assert re.search(r'class="substitute-original"[^>]*>\(A2-id\) A2-original', index)
    assert re.search(r'class="substitute-replacement"[^>]*>A2-substitute', index)
    # This test combines <em> in the original and CSS, which is probably not needed:
    assert re.search(r'class="substitute-original"[^>]*>\(A3-id\) ?<em>A3-original', index)


def test_mode_original(doc1_original):
    index = doc1_original['index']
    assert 'A2-original' in index
    assert 'A2-substitute' not in index

    assert 'A10.1-original' in index
    assert 'A11.1-original' in index
    assert 'A11.2-substitute' not in index

def test_original_inline_markup(doc1_original):
    index = doc1_original['index']
    assert '<em>A4-original</em>' in index

    assert '<em>A10.2-original</em>' in index
    assert '<em>A11.2-original</em>' in index



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


def test_sublist(doc1_default):
    sub_list = doc1_default['sub-list']
    assert 'A1-id' in sub_list
    assert 'A1-original' in sub_list
    assert 'A2-id' in sub_list
    assert 'A2-original' in sub_list
    assert 'A2-substitute' in sub_list


def test_make_sub_rst():
    import sphinx_ext_substitution
    from sphinx_ext_substitution import make_sub_rst
    id_ = 'AAAA'
    text = 'BBBB'
    output = make_sub_rst(id_, text)
    assert output.startswith(':sub:`')
    assert output.endswith("`")
    assert id_ in output
    assert text in output
    content = output[6:-1]  # stripping :sub:` and ` from it
    m = sphinx_ext_substitution.substitution.id_re.match(content)
    assert m
    assert m.group(1) == id_
    assert content[m.end():] == text
