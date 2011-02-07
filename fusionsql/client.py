# Copyright 2010 Dan Colish
# All rights reserved.
#
# This file is part of 'fusionsql' and is distributed under the BSD license.
# See LICENSE for more details.
"""
Connection client for FusionTables
==================================

simple client for fusion tables using OAuth

copyright 2010 Dan Colish <dcolish@gmail.com>

See LICENSE for more detail
"""

import atexit
import csv
from itertools import ifilter
from os.path import expanduser
import readline

from tableformatter import indent

from .driver import connect
from .exception import DatabaseError, OperationalError


class CompleteSQL(object):
    words = ['SELECT', 'INSERT', 'FROM', 'INTO', 'VALUES', 'TABLE',
             'DELETE', 'UPDATE', 'LIMIT', 'ORDER BY', 'GROUP BY', 'WHERE'
             'AND', 'OR', 'SET', 'ASC', 'DESC', 'OFFSET', 'CREATE', 'SHOW',
             'TABLES', 'DESCRIBE', 'DROP']

    def __init__(self, tables=None):
        self.tables = tables

    def complete(self, text, state):
        suggestions = map(lambda x: x + " ",
                     ifilter(lambda x: x.startswith(text),
                              self.words + self.tables)) + [None]
        return suggestions[state]


class FusionClient(object):
    def __init__(self, histfile="~/.fusionsql.history"):
        self.histfile = expanduser(histfile)

    def write_hist(self, filename):
        readline.write_history_file(filename)

    def parse(self, response, pprint):
        try:
            if pprint:
                reader = csv.reader(response)
                return indent([x for x in reader], hasHeader=True)
            else:
                return csv.DictReader(response)
        except Exception, e:
            print e
            raise Exception(e)

    def run(self):
        sqler = connect("dsn")
        sqler.build_tables()
        readline.parse_and_bind("tab: complete")
        readline.set_completer(CompleteSQL(sqler.tables.keys()).complete)
        atexit.register(self.cleanup)
        cur = sqler.cursor()

        try:
            readline.read_history_file(expanduser(self.histfile))
        except IOError:
            pass

        while True:
            try:
                query = raw_input("> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                break

            if query:
                try:
                    print self.parse(cur.execute(query), True)
                except DatabaseError, e:
                    print e
                except OperationalError, e:
                    print e

    def cleanup(self):
        self.write_hist(self.histfile)
        print


def run_cli():
    client = FusionClient("~/.fusionsql.history")
    client.run()


if __name__ == '__main__':
    run_cli()
