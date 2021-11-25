.. Test documentation master file, created by
   sphinx-quickstart on Tue Jun 25 20:00:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Test document
=============

.. toctree::

   sub-list

Roles
-----

No ID: :sub:`A0-original`

No replacement: :sub:`A1-id: A1-original`

Replacement: :sub:`A2-id: A2-original`

No replacement (emphasis): :sub:`A3-id: *A3-original*`

Replacement (emphasis): :sub:`A4-id: *A4-original*`

No replacement (emphasis and no emphasis): :sub:`A5-id: *A5-original1* A5-original2`

No content: :sub:`(A6.1-id)` :sub:`A6.2-id:`

No replacement (preformatted): :sub:`A7-id: \`\`A7-original\`\``

Replacement (preformatted): :sub:`A8-id: \`\`A8-original\`\``

Directive with no replacement
-----------------------------

.. sub:: A10-id

   A10.1-original

   *A10.2-original*

Directive with replacement
--------------------------

.. sub:: A11-id

   A11.1-original

   *A11.2-original*

Directive with no content
-------------------------

.. sub:: A12-id
