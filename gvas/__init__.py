# gvas
# The simulation library, handily named gvas for simple namespacing.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Nov 03 17:02:44 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
The simulation library, handily named gvas for simple namespacing.
"""

##########################################################################
## Imports
##########################################################################


##########################################################################
## Module Info
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0,
}


def get_version(short=False):
    """
    Prints the version.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)

##########################################################################
## Package Version
##########################################################################

__version__ = get_version()
