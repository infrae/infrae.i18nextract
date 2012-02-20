# Copyright (c) 2010-2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from optparse import OptionParser
import os
import re

from zope.configuration.name import resolve
from infrae.i18nextract.utils import load_products


def process_files(path, options):
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
            if options.merge:
                print 'Merging language "%s", domain "%s"' % (language, domain)
                os.system('msgmerge -N -U %s %s' %(filename, pot_path))
            if options.compile:
                compiled_filename = os.path.splitext(filename)[0] + '.mo'
                print 'Compiling language "%s", domain "%s".' % (
                    language, domain)
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
                if options.merge:
                    print 'Merging language "%s", domain "%s"' % (
                        language, domain)
                    os.system('msgmerge -N -U %s %s' %(filename, pot_path))
                if options.compile:
                    compiled_filename = os.path.splitext(filename)[0] + '.mo'
                    print 'Compiling language "%s", domain "%s".' % (
                        language, domain)
                    os.system('msgfmt -o %s %s' % (compiled_filename, filename))


def merge(output_package, products):
    """Merge translations for the given packages.
    """
    parser = OptionParser()
    parser.add_option(
        "-p", "--path", dest="path",
        help="path where the translation to merge are")
    parser.add_option(
        "-c", "--compile", dest="compile", action="store_true",
        help="compile all translations files")
    parser.add_option(
        "-m", "--merge", dest="merge", action="store_true",
        help="merge all templates to in all translation files")
    (options, args) = parser.parse_args()

    if options.path:
        process_files(options.path, options)
    else:
        if products:
            load_products(products)
        python_package = resolve(output_package)
        path = os.path.dirname(python_package.__file__)
        for i18n_part in ('i18n', 'locales'):
            i18n_path = os.path.join(path, i18n_part)
            if os.path.isdir(i18n_path):
                print "Processing package %s/%s..." % (
                    output_package, i18n_part)
                process_files(i18n_path, options)


def egg_entry_point(kwargs):
    return merge(**kwargs)
