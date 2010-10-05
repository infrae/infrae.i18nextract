# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from optparse import OptionParser
import os
import re

from zope.configuration.name import resolve


def merge_files(path, compile_translations=False):
    po_file_reg = re.compile('(.*)-([a-z]{2})\.po$')
    for filename in os.listdir(path):
        filename = os.path.join(path, filename)
        if filename.endswith('.po'):
            match = po_file_reg.search(filename)
            if not match:
                # not a .po file
                continue
            domain = match.group(1)
            language = match.group(2)
            pot_path = os.path.join(path, '%s.pot' % domain)
            print 'Merging language "%s", domain "%s"' % (language, domain)
            os.system('msgmerge -N -U %s %s' %(filename, pot_path))
            if compile_translations:
                compiled_filename = os.path.splitext(filename)[0] + '.mo'
                os.system('msgfmt -o %s %s' % (compiled_filename, filename))

    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')

        # Make sure we got a language directory
        if not os.path.isdir(lc_messages_path):
            continue

        for filename in os.listdir(lc_messages_path):
            if filename.endswith('.po'):
                pot_path = os.path.join(path, filename + 't')
                domain = '.'.join(filename.split('.')[:-1])
                filename = os.path.join(lc_messages_path, filename)
                print 'Merging language "%s", domain "%s"' % (language, domain)
                os.system('msgmerge -N -U %s %s' %(filename, pot_path))
                if compile_translations:
                    compiled_filename = os.path.splitext(filename)[0] + '.mo'
                    os.system('msgfmt -o %s %s' % (compiled_filename, filename))


def merge(output_package):
    """Merge translations for the given packages.
    """

    parser = OptionParser()
    parser.add_option(
        "-p", "--path", dest="path",
        help="path where the translation to merge are")
    parser.add_option(
        "-c", "--compile", dest="compile", action="store_true",
        help="compile translations as well")
    (options, args) = parser.parse_args()

    if options.path:
        merge_files(options.path, options.compile)
    else:
        python_package = resolve(output_package)
        path = os.path.dirname(python_package.__file__)
        i18n_path = os.path.join(path, 'i18n')
        if os.path.isdir(i18n_path):
            print "Merging package %s/i18n..." % output_package
            merge_files(i18n_path, options.compile)


def egg_entry_point(kwargs):
    return merge(**kwargs)
