Data Model
====================

The basic objects of the protocol as ``users``, ``contributions`` and ``evaluations``.


Users
------------

Users have ``tokens``, a number representing the amount of `ownership` of a contract,  
and ``reputation``, a number that represents the user reputation within the system.

.. literalinclude:: inc/user_json.inc

Contributions
-----------------

A contribution has a ``contributor`` (which is the user that has made the contribution),
a ``score`` which represents how much the contribution has been valued
by the community, and ``engaged_reputation``, a value between 0 and 1 
that represents the sum of the reputation of the users that have 
evaluated the contribution.

.. literalinclude:: inc/contribution_json.inc


Evaluations
----------------------

An evaluation of a contribution has an ``evaluator``, which is the user that
has made the evaluation, the ``contribution`` that the evaluation pertains to,
and a ``value``.

.. literalinclude:: inc/evaluation_json.inc
