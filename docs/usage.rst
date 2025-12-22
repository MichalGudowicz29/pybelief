Quickstart
==========

Install
-------

.. code-block:: bash

   pip install -e .

Basic fusion
------------

.. code-block:: python

   from pybelief.core.belief_mass import BeliefMass
   from pybelief.fusion import dempster

   m1 = BeliefMass({frozenset("A"): 0.6, frozenset("B"): 0.4})
   m2 = BeliefMass({frozenset("A"): 1.0})

   fused = dempster.combine(m1, m2)
   print(fused)

Multiple sources
----------------

.. code-block:: python

   from pybelief.fusion import pcr

   sources = [
       BeliefMass({frozenset("A"): 0.7, frozenset("B"): 0.3}),
       BeliefMass({frozenset("A"): 1.0}),
       BeliefMass({frozenset("A"): 1.0}),
   ]

   fused = pcr.combine_multiple(sources)
   print(fused)
