"""
Commandline table formatter

Original
Copyright 2004 George Sakkis

Modified 2010 Dan Colish <dcolish@gmail.com>

see LICENSE for more detail
"""

## {{{ http://code.activestate.com/recipes/267662/ (r7)


def indent(rows, hasHeader=False, headerChar='-', delim=' | ',
           justify='left', separateRows=False, prefix='', postfix=''):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column.
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       """
    output = []

    # break each logical row into one or more physical ones
    logicalRows = [item or '' for item in rows]

    # columns of physical rows
    columns = map(None, *logicalRows)

    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column])
                 for column in columns]

    # select the appropriate justify method
    justify = {'center': str.center,
               'right': str.rjust,
               'left': str.ljust}[justify.lower()]

    rowSeparator = headerChar * (
        len(prefix) + len(postfix) + sum(maxWidths) + len(delim) * \
            (len(maxWidths) - 1))

    if separateRows:
        output += [rowSeparator]

    for row in logicalRows:
        output += [prefix +
                   delim.join([justify(str(item), width)
                               for (item, width)
                               in zip(row, maxWidths)]) + postfix]

        if separateRows or hasHeader:
            output += [rowSeparator]
            hasHeader = False

    return '\n'.join(output)
