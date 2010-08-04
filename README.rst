FusionSQL
=========

A simple command line client for Google Fusion Tables

FusionSQL class can also be used within an application to query
the Fusion Table databases

For commands see the documetation at `Google`_

Code is available on `github`_


Using FusionSQL
===============

Here is an example of calling the FusionSQL class from your code::

 from fusionsql.client import FusionSQL

 fsql = FusionSQL()

 result = fsql.query("SELECT ROWID, 'Police District'"
                     " FROM 224239 WHERE Neighborhood = ''")

  rows = [x for x in result]
  fails = []
  for row in rows:
      neighborhood_query = ("SELECT Neighborhood FROM 224239"
                            "WHERE Neighborhood not equal to '' "
                            "AND 'Police District' = '%s' LIMIT 1")
      print row
      try:
          neighborhood = fsql.query(
              neighborhood_query % row['Police District']).next()
          if neighborhood['Neighborhood']:
              fsql.query(
                  "UPDATE 224239 SET Neighborhood = '%s' WHERE ROWID = '%s'" %
                  (neighborhood['Neighborhood'].replace("'", "\'"),
                  row['rowid']))
              print 'Update: ' + row['rowid']
      except StopIteration:
          fsql.query(
              "DELETE FROM 224239 WHERE ROWID = '%s'" % row['rowid'])


.. _`github`: http://github.com/dcolish/python-fusion-tables
.. _`Google`: http://code.google.com/apis/fusiontables/docs/developers_guide.html
