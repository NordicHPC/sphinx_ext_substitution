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
- Both role and directive support.



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

       (optional content)


This directive works analogously to the role, with an ID of
``ssh_clarification``.  If content is missing, there will be nothing
in the case that no substitution is defined, so in this case when used
without content it can be used to add in an extra content in just some
places.  If the directive had content, then it would work the same as
the first example.

As a reminder, in Docutils/Sphinx, a role is inline text and a
directive is a paragraph-level structure.



Currently there are two Sphinx variables defined:

* ``substitute_mode``: One of ``original``, ``replace`` (the default),
  or ``both`` (for including both marked up to compare).

* ``substitute_path`` is a path to search for replacement variables,
  either ``$ID.rst`` or ``*.yaml`` with an key of ``$ID``.


Development and maintenance
---------------------------

This is still "under development" and doesn't yet work.  This also a
call for help (this is really being developed without enough
Sphinx/Docutils knowledge): it's not too late to make major changes.
