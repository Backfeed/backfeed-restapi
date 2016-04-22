Data Model
====================

The basic objects of the protocol as ``users``, ``contributions`` and ``evaluations``.


Users
------------

Users have ``tokens``, a number representing the amount of `ownership` of a contract,  
and ``reputation``, a number between 0 and 1 that represents the fraction of user reputation with 
respect to the total reputation in the system: ::

   {
       'id': 123,
       'tokens': 11.3,
       'reputation': 0.03
    }


Contributions
-----------------

A contribution has a ``contributor`` (which is the user that has made the contribution),
a ``score`` which represents how much the contribution has been valued
by the community, and ``engaged_reputation``, a value between 0 and 1 
that represents the sum of the reputation of the users that have 
evaluated the contribution. ::

    {
        'id': 12345,
        'score': 0.30, 
        'engaged_reputation': 0.4, 
        'type': 'article',
        'contributor' : {
           'id': 123,
           'tokens': 11.3,
           'reputation': 0.03
        }
    }



Evaluations
----------------------

An evaluation of a contribution has an ``evaluator``, which is the user that
has made the evaluation, the ``contribution`` that the evaluation pertains to,
and a ``value``. ::

    {
        'id': 1234545,
        'value': 1,
        'evaluator' : {
           'id': 123,
           'tokens': 11.3,
           'reputation': 0.03
        },
        'contribution': {
            'id': 12345,
            'score': 0.30, 
            'engaged_reputation': 0.4
        }
    }
