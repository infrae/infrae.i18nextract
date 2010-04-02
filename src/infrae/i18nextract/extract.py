#!/usr/bin/env python2.4
##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
#
# Hacked up by Guido Wesdorp to be less Zope 3 specific (e.g. it doesn't break
# on space-seperated tal:attributes) and doesn't try to parse zcml stuff 
# (which is not a good thing per se, but does remove a lot of dependencies)
#
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Program to extract internationalization markup from Python Code,
Page Templates and ZCML.

This tool will extract all findable message strings from all
internationalizable files in your Zope 3 product. It only extracts message ids
of the specified domain. It defaults to the 'zope' domain and the zope
package.

Note: The Python Code extraction tool does not support domain
      registration, so that all message strings are returned for
      Python code.

Note: The script expects to be executed either from inside the Zope 3 source
      tree or with the Zope 3 source tree on the Python path.  Execution from
      a symlinked directory inside the Zope 3 source tree will not work.

Usage: i18nextract.py [options]
Options:
    -h / --help
        Print this message and exit.
    -d / --domain <domain>
        Specifies the domain that is supposed to be extracted (i.e. 'zope')
    -p / --path <path>
        Specifies the package that is supposed to be searched
        (i.e. 'zope/app')
    -o dir
        Specifies a directory, relative to the package in which to put the
        output translation template.

$Id: i18nextract,v 1.3 2004/11/26 14:38:48 faassen Exp $
"""
import os, sys, getopt

SOFTWARE_HOME = os.path.dirname(__file__)
INSTANCE_HOME = os.path.dirname(__file__)

def usage(code, msg=''):
    # Python 2.1 required
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

def app_dir():
    try:
        import zope
    except ImportError:
        # Couldn't import zope, need to add something to the Python path

        # Get the path of the src
        path = os.path.abspath(os.getcwd())
        while not path.endswith('src'):
            parentdir = os.path.dirname(path)
            if path == parentdir:
                # root directory reached
                break
            path = parentdir
        sys.path.insert(0, path)

        try:
            import zope
        except ImportError:
            usage(1, "Make sure the script has been executed "
                     "inside Zope 3 source tree.")

    return os.path.dirname(zope.__file__)

def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'hd:p:o:',
            ['help', 'domain=', 'path=', 'python-only'])
    except getopt.error, msg:
        usage(1, msg)

    domain = 'zope'
    path = app_dir()
    include_default_domain = True
    output_dir = None
    python_only = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-d', '--domain'):
            domain = arg
            include_default_domain = False
        elif opt in ('-o', ):
            output_dir = arg
        elif opt in ('--python-only',):
            python_only = True
        elif opt in ('-p', '--path'):
            if not os.path.exists(arg):
                usage(1, 'The specified path does not exist.')
            path = arg
            # We might not have an absolute path passed in.
            if not path == os.path.abspath(path):
                cwd = os.getcwd()
                # This is for symlinks. Thanks to Fred for this trick.
                if os.environ.has_key('PWD'):
                    cwd = os.environ['PWD']
                path = os.path.normpath(os.path.join(cwd, arg))

    # When generating the comments, we will not need the base directory info,
    # since it is specific to everyone's installation
    src_start = path.rfind('lib/python')
    if src_start == -1:
        base_dir = path
    else:
        base_dir = path[:src_start]

    output_file = domain+'.pot'
    if output_dir:
        output_dir = os.path.join(path, output_dir)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        output_file = os.path.join(output_dir, output_file)

    print "base path: %r\nsearch path: %r\ndomain: %r\noutput file: %r" \
        % (base_dir, path, domain, output_file)

    from zope.app.locales.extract import POTMaker, \
         py_strings, tal_strings
    from formulator_extract import formulator_strings
    from metadata_extract import metadata_strings
    
    maker = POTMaker(output_file, path)
    maker.add(py_strings(path, domain), base_dir)
    if not python_only:
        maker.add(tal_strings(path, domain, include_default_domain), base_dir)
        maker.add(formulator_strings(path, domain), base_dir)
        maker.add(metadata_strings(path, domain), base_dir)
    maker.write()


def run():
    # This removes the script directory from sys.path, which we do
    # since there are no modules here.
    #
    basepath = filter(None, sys.path)

    sys.path[:] = [os.path.join(INSTANCE_HOME, "lib", "python"),
                   SOFTWARE_HOME] + basepath

    main()


if __name__ == '__main__':
    run()
