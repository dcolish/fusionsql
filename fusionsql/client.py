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
from itertools import ifilter
from os.path import expanduser
import readline

from .driver import FusionSQL, QueryException


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


def write_hist(filename):
    readline.write_history_file(filename)


def start_cli():
    sqler = FusionSQL()
    sqler.build_tables()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(CompleteSQL(sqler.tables.keys()).complete)
    atexit.register(write_hist, expanduser("~/.fusionsql.history"))

    try:
        readline.read_history_file(expanduser("~/.fusionsql.history"))
    except IOError:
        pass

    try:
        while True:
            query = raw_input("> ")
            if query:
                try:
                    print sqler.query(query, True)
                except QueryException, e:
                    print e
    except EOFError:
        print


if __name__ == '__main__':
    start_cli()
