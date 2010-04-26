# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import zc.recipe.egg
import zc.buildout.easy_install


SCRIPT_REQUIRES = [
    'zope.configuration',
    'zope.app.locales [extract]',
    'zope.i18nmessageid',
    'infrae.i18nextract']


class Recipe(object):
    """Install scripts
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.options['eggs'] = self.options.get('eggs', '') + '\n' + \
            '\n '.join(SCRIPT_REQUIRES) + \
            '\n ' + options['packages'] + \
            '\n ' + options.get('output-package', '')
        self.packages = filter(lambda v: v, map(
                lambda s: s.strip(), options['packages'].split('\n')))
        self.output_dir = options['output'].strip()
        self.output_package = options.get('output-package', '').strip()
        self.domain = options.get('domain', 'silva').strip()
        paths = [p.strip() for p in options.get('extra_paths', '').split('\n')]
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        """Install the recipe.
        """
        scripts = []
        requirements, ws = self.egg.working_set()
        arguments = {'packages': self.packages,
                     'output_dir': self.output_dir,
                     'output_package': self.output_package,
                     'domain': self.domain}

        scripts.extend(
            zc.buildout.easy_install.scripts(
                [('%s-extract'% self.name,
                  'infrae.i18nextract.extract',
                  'egg_entry_point')],
                ws, self.options['executable'],
                self.buildout['buildout']['bin-directory'],
                arguments = arguments,
                extra_paths = self.egg.extra_paths,
                ))

        arguments = {'output_package': self.output_package,}

        scripts.extend(
            zc.buildout.easy_install.scripts(
                [('%s-merge'% self.name,
                  'infrae.i18nextract.merge',
                  'egg_entry_point')],
                ws, self.options['executable'],
                self.buildout['buildout']['bin-directory'],
                arguments = arguments,
                extra_paths = self.egg.extra_paths,
                ))

        return scripts

    update = install
