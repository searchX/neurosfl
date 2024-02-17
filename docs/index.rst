.. NeuroSFL documentation master file, created by
   sphinx-quickstart on Sat Feb 17 06:20:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NeuroSFL's documentation!
====================================
NeuroSFL ie Neuro SQL inspired Filtering Language is a python package 
that provides a simple and easy to use language to quickly write filters
for information retrieval systems. (Currently only supporting Elasticsearch)

Installation
------------

[Coming Soon] Install the ``neurosfl`` package with `pip
<https://pypi.org/project/neurosfl>`_:

.. code-block:: console

    $ pip install neurosfl

Or install the latest package directly from github

.. code-block:: console

    $ pip install git+https://github.com/searchX/neurosfl

Example Usage
-------------
Assuming data to be in format:

.. code-block:: json

   {
      "name": "John Doe",
      "age": 24,
      "height": 4.5,
      "weight": 60,
      "address": "123, Main Street, New York",
      "occupation": "Engineer",
      "hobbies": ["reading", "swimming", "travelling"]
   }

import the package and create a filter

.. code-block:: python

   from neurosfl.main import parse_from_string
   # ... write a filter

1. Simple filter to get all records where age is greater than 20

.. code-block:: python
   
   print(parse_from_string("age > 20"))
   # Output: {'bool': {'must': {'range': {'age': {'gt': 20}}}}

2. Filter to get all records where age is greater than 20 and height is less than 5

.. code-block:: python

   print(parse_from_string("age > 20 and height < 5"))
   # Output: {'bool': {'must': [{'bool': {'must': {'range': {'age': {'gt': 20}}}}}, {'bool': {'must': {'range': {'height': {'lt': 5}}}}}]}}

3. Get all software engineers

.. code-block:: python

   print(parse_from_string("occupation = 'Engineer'"))
   # Output: {'bool': {'must': {'term': {'occupation': {'value': 'Engineer', 'boost': 1.0}}}}}

4. Can have optional starting with 'WHERE'

.. code-block:: python

   print(parse_from_string("WHERE age > 20 and height < 5"))
   # Output: {'bool': {'must': [{'bool': {'must': {'range': {'age': {'gt': 20}}}}}, {'bool': {'must': {'range': {'height': {'lt': 5}}}}}]}}

5. Nested filters

.. code-block:: python

   print(parse_from_string("age > 20 and (height < 5 or weight > 70) or (age < 20 and weight > 70)"))
   # Output: {'bool': {'should': [{'bool': {'must': [{'bool': {'must': {'range': {'age': {'gt': 20}}}}}, {'bool': {'should': [{'bool': {'must': {'range': {'height': {'lt': 5}}}}}, {'bool': {'must': {'range': {'weight': {'gt': 70}}}}}]}}]}}, {'bool': {'must': [{'bool': {'must': {'range': {'age': {'lt': 20}}}}}, {'bool': {'must': {'range': {'weight': {'gt': 70}}}}}]}}]}}

See more usage and sample codes in package documentations and tests

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
