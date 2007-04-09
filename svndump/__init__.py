#===============================================================================
#
# Copyright (C) 2003 Martin Furter <mf@rola.ch>
#
# This file is part of SvnDumpTool
#
# SvnDumpTool is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# SvnDumpTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SvnDumpTool; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#
#===============================================================================

#import 
__all__ = [ "common", "node", "file", "diff", "merge", "eolfix", "tools" ]

import re
import common
from file import SvnDumpFile

__doc__ = """A package for processing subversion dump files."""
__version = "0.4.0"

def copy_dump_file( srcfile, dstfile, transformer=None ):
    """
    Copy a dumpfile.

    @type srcfile: string
    @param srcfile: Source filename.
    @type dstfile: string
    @param dstfile: Destination filename.
    @type transformer: class with method transform(dump)
    @param transformer: A class to perform a transformation on each revision, or None.
    """

    # SvnDumpFile classes for reading/writing dumps
    srcdmp = SvnDumpFile()
    dstdmp = SvnDumpFile()

    # open source file
    srcdmp.open( srcfile )

    hasrev = srcdmp.read_next_rev()
    if hasrev:
        # create the dumpfile
        dstdmp.create_like( dstfile, srcdmp )
        # now copy all the revisions
        while hasrev:
            if transformer != None:
                transformer.transform( srcdmp )
            dstdmp.add_rev_from_dump( srcdmp )
            hasrev = srcdmp.read_next_rev()
    else:
        print "no revisions in the source dump '%s' ???" % srcfile

    # cleanup
    srcdmp.close()
    dstdmp.close()
