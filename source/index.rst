.. paper-digest documentation master file, created by
   sphinx-quickstart on Thu Jul 25 19:33:29 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Paper Digest
============

.. toctree:: 
   :glob:
   :caption: Table of Contents:
   :maxdepth: 1

   paper/*
   terminology


Pseudocode
----------
.. pcode::
   :linenos:

    % This quicksort algorithm is extracted from Chapter 7, Introduction to Algorithms (3rd edition)
    \begin{algorithm}
    \caption{Quicksort}
    \begin{algorithmic}
    \PROCEDURE{Quicksort}{$A, p, r$}
        \IF{$p < r$}
            \STATE $q = $ \CALL{Partition}{$A, p, r$}
            \STATE \CALL{Quicksort}{$A, p, q - 1$}
            \STATE \CALL{Quicksort}{$A, q + 1, r$}
        \ENDIF
    \ENDPROCEDURE
    \PROCEDURE{Partition}{$A, p, r$}
        \STATE $x = A[r]$
        \STATE $i = p - 1$
        \FOR{$j = p$ \TO $r - 1$}
            \IF{$A[j] < x$}
                \STATE $i = i + 1$
                \STATE exchange
                $A[i]$ with     $A[j]$
            \ENDIF
            \STATE exchange $A[i]$ with $A[r]$
        \ENDFOR
    \ENDPROCEDURE
    \end{algorithmic}
    \end{algorithm}


MarkMap
-------
.. raw:: html

   <iframe src="_static/markmap/demo.html" width="100%" height="500px"></iframe>