"""
Commandline table formatter

Original
Copyright 2004 George Sakkis

Modified 2010 Dan Colish <dcolish@gmail.com>

see LICENSE for more detail
"""

## {{{ http://code.activestate.com/recipes/267662/ (r7)


from cStringIO import StringIO


def justify(justification, item, width):
    str_justify = {'center': str.center,
                   'right': str.rjust,
                   'left': str.ljust}
    fn = str_justify.get(justification, 'left')
    return fn(str(item), width)


def indent(rows, hasHeader=False, headerChar='-', delim=' | ',
           justification='left', separateRows=False, prefix='', postfix=''):
    """Indents a table by column.

       :param rows: A sequence of sequences of items, one sequence per row.

       :param hasHeader: True if the first row consists of the columns' names.

       :param headerChar: Character to be used for the row separator line
                          (if hasHeader==True or separateRows==True).

       :param delim: The column delimiter.

       :param justify: Determines how are data justified in their column.
                       Valid values are 'left','right' and 'center'.

       :param separateRows: True if rows are to be separated by a line
                            of 'headerChar's.

       :param prefix: A string prepended to each printed row.

       :param postfix: A string appended to each printed row.
       """
    output = StringIO()

    # get the maximum of each column by the string length of its items
    maxWidths = [max(map(len, column)) for column in zip(*rows)]

    rowSeparator = headerChar * (
        len(prefix) + len(postfix) + sum(maxWidths) + len(delim) * \
            (len(maxWidths) - 1))

    if separateRows:
        print >> output, rowSeparator

    for row in rows:
        print >> output, ''.join((prefix + delim.join((
                        justify(justification, item, width)
                        for (item, width)
                        in zip(row, maxWidths))) + postfix))
        if separateRows or hasHeader:
            print >> output, rowSeparator
            hasHeader = False

    final = output.getvalue()
    output.close()
    del output
    return final
