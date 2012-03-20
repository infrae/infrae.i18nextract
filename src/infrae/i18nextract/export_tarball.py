# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from optparse import OptionParser
import os
import sys
import tarfile

from zope.configuration.name import resolve

from infrae.i18nextract.extract import extract


def export_tarball(packages, output_dir, package, domain):
    """Create a tarball for uploading to Launchpad
    """
    tar_file = 'launchpad-upload.tar.gz'

    parser = OptionParser()
    parser.add_option(
        "-o", "--output", dest="output_dir",
        help="alternate output directory for the created tarball")
    parser.add_option(
        "-e", "--extract", action="store_true", dest="extract",
        help="extract i18n strings into silva.pot and place in tarball")
    parser.add_option(
        "-p", "--package", action="store_true", dest="output_package",
        help="extract to the output package, only in combination with '-e'")
    parser.add_option(
        "-n", "--name", dest="name", default=tar_file,
        help="alternate name for the created tarball, default is %s" % tar_file)
    (options, args) = parser.parse_args()

    if options.name != tar_file:
        if not options.name.endswith('.tar.gz'):
            options.name += '.tar.gz'
        tar_file = options.name

    if options.output_dir:
        if not os.path.exists(options.output_dir):
            print "Selected directory doesn't exists: %s" % options.output_dir
            return
        tar_file = os.path.join(options.output_dir, tar_file)
    elif output_dir:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        tar_file = os.path.join(output_dir, tar_file)

    if os.path.isfile(tar_file):
        print "The export file (%s) already exists\nRemove it before "\
              "running the script or use a different name" % tar_file
        return

    tar = tarfile.open(tar_file, "w:gz")

    # Add pot file if requested
    if options.extract:
        sys.argv.remove('-e')
        if '-n' in sys.argv:
            sys.argv.pop( sys.argv.index('-n') + 1 )
            sys.argv.pop( sys.argv.index('-n') )

        pot_file = extract(packages, output_dir, package, domain)
        tar.add(pot_file, arcname='silva.pot')

    # Loop through the translations dir, copy language files to the tar
    translations = os.path.join(resolve(package).__path__[0], 'i18n')
    for language in os.listdir(translations):
        po_file = os.path.join(translations, language, 'LC_MESSAGES','silva.po')

        if not os.path.isfile(po_file):
            continue

        arcname = os.path.join(domain, '%s-%s.po' % (domain, language))
        tar.add(po_file, arcname=arcname)

    tar.close()


def egg_entry_point(kwargs):
    return export_tarball(**kwargs)
