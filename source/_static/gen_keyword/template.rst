Terminology
===========

.. list-table:: 
   :widths: 10 30 60
   :header-rows: 1

   * - Abbreviation
     - KeyTerm
     - Definition
   {% for keyterm in keyterms %}
   * - {{ keyterm.Abbreviation }}
     - {{ keyterm.Term }}
     - {{ keyterm.Definition }}
   {% endfor %}

References
----------
.. bibliography::
    :filter: docname in docnames
