REST API for the backfeed-protocol
.. image:: https://travis-ci.org/Backfeed/backfeed-restapi.svg?branch=master
    :target: https://travis-ci.org/Backfeed/backfeed-restapi
===================================



Installation
-------------------------


You need pip installed::

    sudo apt-get install python-pip

You can now either directly install from the github repository: ::

     pip install git+https://github.com/Backfeed/backfeed-restapi.git


Starting a server
------------------

First you need to create an settings file. You can download it from the git repository: ::
    
    wget https://raw.githubusercontent.com/Backfeed/backfeed-restapi/master/development.ini

You can then start the server like this: ::

    pserve development.ini 

The default settings will use a database that runs completely in memory, so you will loose any changes after restarting the server.


Contributing
-------------


