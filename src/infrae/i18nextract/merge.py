# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from optparse import OptionParser
import sys
import os
import re

from zope.configuration.name import resolve


def merge_files(path):
    po_file_reg = re.compile('(.*)-([a-z]{2})\.po$')
    for filename in os.listdir(path):
        filename = os.path.join(path, filename)
        if filename.endswith('.po'):
            match = po_file_reg.search(filename)
            if not match:
                # not a .po file
                continue
            language = match.group(2)
            if language == 'en':
                # we assume english is default, so bail out
                continue
            domain = match.group(1)
            pot_path = os.path.join(path, '%s.pot' % domain)
            print 'Merging language "%s", domain "%s"' % (language, domain)
            os.system('msgmerge -N -U %s %s' %(filename, pot_path))

    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')

        # English is the default for Zope, so ignore it
        if language == 'en':
            continue

        # Make sure we got a language directory
        if not os.path.isdir(lc_messages_path):
            continue

        msgs = []
        for domain_file in os.listdir(lc_messages_path):
            if domain_file.endswith('.po'):
                domain_path = os.path.join(lc_messages_path, domain_file)
                pot_path = os.path.join(path, domain_file+'t')
                domain = domain_file.split('.')[0]
                print 'Merging language "%s", domain "%s"' %(language, domain)
                os.system('msgmerge -N -U %s %s' %(domain_path, pot_path))


def merge(output_package):
    """Merge translations for the given packages.
    """

    parser = OptionParser()
    parser.add_option(
        "-p", "--path", dest="path",
        help="path where the translation to merge are")
    (options, args) = parser.parse_args()

    if options.path:
        merge_files(options.path)
    else:
        python_package = resolve(output_package)
        path = os.path.dirname(python_package.__file__)
        i18n_path = os.path.join(path, 'i18n')
        if os.path.isdir(i18n_path):
            print "Merging package %s/i18n..." % output_package
            merge_files(i18n_path)


def egg_entry_point(kwargs):
    return merge(**kwargs)
