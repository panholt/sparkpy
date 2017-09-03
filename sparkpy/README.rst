sparkpy: A python3 module for Cisco Spark APIs
==============================================

sparkpy is an module for Cisco Spark APIs written for python3.

Usage is simple:

.. code-block:: python

    >>> from sparkpy import Spark
    >>> spark = Spark()  # Use the SPARK_TOKEN environment varible
    >>> # Alternatively spark = Spark('MY TOKEN')
    >>> for room in spark.rooms:
    ... print(f'{room.title}')
    >>> room = spark.create_room('Sample Room')
    >>> room.add_member('email@isp.com')

