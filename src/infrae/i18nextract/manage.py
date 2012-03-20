# Copyright (c) 2010-2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from optparse import OptionParser
import os
import re
import tarfile

from zope.configuration.name import resolve
from infrae.i18nextract.utils import load_products


po_file_reg = re.compile('(.*)-([a-zA-Z_]{2,5})\.po$')


def import_tarball(path, options, package):
    translations_path = resolve(package).__path__[0]

    tar = tarfile.open(path, "r:gz")
    for name in tar.getnames():
        if name.endswith('.po'):
            match = po_file_reg.search(name.split('/')[-1])
            if not match:
                continue # not a .po file
            domain = match.group(1)
            language = match.group(2)

            language_path = os.path.join(translations_path, 'i18n', language)
            if not os.path.isdir(language_path):
                os.mkdir(language_path)
            lc_messages_path = os.path.join(language_path, 'LC_MESSAGES')
            if not os.path.isdir(lc_messages_path):
                os.mkdir(lc_messages_path)
            po_path = os.path.join(lc_messages_path, '%s.po' % domain)
            mo_path = os.path.splitext(po_path)[0] + '.mo'

            content = tar.extractfile(name).read()
            with open(po_path, 'w') as po_file:
                print 'Extracting language "%s", domain "%s"' % (
                        language, domain)
                po_file.write(content)

            if options.compile:
                print 'Compiling language "%s", domain "%s".' %(language,domain)
                os.system('msgfmt -o %s %s' % (mo_path, po_path))

    tar.close()


def process_files(path, options):
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
        "-t", "--tarball", dest="tarball", action="store_true",
        help="the translations are packed in a tarball")
    parser.add_option(
        "-c", "--compile", dest="compile", action="store_true",
        help="compile all translation files")
    parser.add_option(
        "-m", "--merge", dest="merge", action="store_true",
        help="merge all templates to in all translation files")
    (options, args) = parser.parse_args()

    if options.tarball:
        if not options.path or not os.path.isfile(options.path):
            print "You need to specify the location of the tarball"
            return
        import_tarball(options.path, options, output_package)
    elif options.path:
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
