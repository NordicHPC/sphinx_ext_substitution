Sphinx extension for power substitutions
========================================

`Sphinx <https://www.sphinx-doc.org/>`__ (and `Docutils
<http://docutils.sourceforge.net/>`__) provide a way to template
variables into your documentation, but it can be kind of limited.
This Sphinx extension provides a powerful way to manage a master set
of documentation with local-specific variations.  **Logical
management** is a key design consideration: it's easy to make some
variable substitutions, but harder to keep them up to date when you
make a long-running fork!

Features include:

- Default values can also be included inline and replaced only if a
  replacement value is defined.
- Search paths for variable replacements: hierarchical variable
  substitutions, group and then local customizations supported.
- Multiple compilation mode: original, with substitutions, or both.
  In the "both" mode, both the original and substituted are shown with
  highlighting, so that you can easily compare the current original
  values with your current substitute values.
- Both role (inline) and directive (paragraph level) support.



Usage examples
--------------

As a role::

  SSH to :sub:`(hostname) triton.aalto.fi`

We see the ReST role is named ``sub`` (which conflicts with
"subscript", maybe we should change that) and an ID of ``hostname``.
If there is a file called ``hostname.rst`` in the search path or a
file with a ``.yaml`` extension with a ``hostname`` key in the search
path, it will substitute that value into this place.  If this value
doesn't exist, it will use the original (or remove it if the original
is empty).

As a directive::

   .. sub:: ssh_clarification

This directive works analogously to the role, with an ID of
``ssh_clarification``.  There is no default content in this example,
which means that nothing is inserted unless a replacement is defined ,
so in this case when used without content it can be used to add in an
extra content in just some versions.  (There could be default content,
too.)  If the directive had content, then it would work the same as
the first example.

As a reminder, in Docutils/Sphinx, a role is inline text and a
directive is a paragraph-level structure.

There are three run modes, controlled by the ``substitution_mode``
configuration option:

* ``replace``: Use the replacements if defined or else the original,
  with no special markup.  This is the default mode and does what you
  expect for normal use.

* ``both``: Show *both* the ID, original value, and the replacement
  value with distinguishing markup (HTML only).  This can be used to
  compare your local version with the latest upstream. to see what
  needs to be updated - or what substitutions are available and should
  be used.

* ``original``: Show only the original text without any replacements.

Finally, there is a ``sub-list`` directive::

  .. sub-list::

This directive is replaced with a table that contains all substitution
IDs, original values, and replacements that have been used in the
document.


When searching for replacement values:

1. First, each item in the search path (configuration option
   ``substitute_path``) is searched.

   a. If it's a file, load it as YAML (see below)

   b. If it's a directory, go to step 2.

2. List the directory and search for files to load.

   a. First, load all ``*.rst`` files.  The ``*`` value is used as the
      replacement ID.

   b. Second, search for all ``*.yaml`` files.  Load them as YAML
      data, which should be a mapping from keys to values.

   c. All values are ``.strip()``\ ped.

3. Use the first-detected value for each ID.  Thus, earlier items in
   the search path take precedence over later ones.


YAML reminder::

  ID1: this is the text for replacement id = ID1
  ID2: |
      This is a block text that preserves newlines.

      The "|" character is what indicates that newlines should be
      preserved.
  ID3: >
      Using the ">" character removes all newlines and runs the block
      text together.


Installation
------------
Install the extension.  Currently not in any package managers, so::

    pip install

Add the extension to your Sphinx ``conf.py`` file::

    extensions = [
        'sphinx_ext_substitution'
    ]

There are no non-trivial dependencies besides PyYAML (which is listed
as a dependency, but if you don't use the YAML feature it isn't
needed).  Sphinx and Docutils are obviously required - our goal is to
support any reasonable version.



Configuration
-------------

Currently there are two Sphinx variables defined:

* ``substitute_mode``: One of ``replace`` (the default), ``original``,
  or ``both``.  See above for the meaning of these values.

* ``substitute_path`` is a path to search for replacement variables,
  keyed by ID.  In Sphinx, this is a list of paths, but if given on
  command with ``-D substitute_path=dir1:dir2``, you can
  colon-separate paths as well.  Each file on this path that ends in
  ``.rst`` or ``.yaml`` is searched for variables.  The default is
  ``.``.

* The environment variable ``SPHINX_EXT_SUBSTITUTION_PATH`` is used
  *before* the ``substitute_path`` configuration option.  Both are
  used if both are given (the env var takes precedence).  There is no
  need for both, but it provides more flexible configuration for
  integration to your build system.



Development and maintenance
---------------------------

Most functonality exists and this is now usable, but not extensively
used yet.  Please send any changes or requests to us.  This was
developed as a first non-trivial Sphinx extension, so any refactorings
to make things better are welcome.

Primary maintainer: Richard Darst, Aalto University.
