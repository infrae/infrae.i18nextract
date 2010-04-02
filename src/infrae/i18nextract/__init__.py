# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import zc.recipe.egg
import zc.buildout.easy_install


SCRIPT_REQUIRES = [
    'zope.configuration',
    'zope.app.locales [extract]',
    'zope.i18n',
    'infrae.i18nextract']


class Recipe(object):
    """Install scripts
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.options['eggs'] = self.options['eggs'] + \
            '\n '.join(SCRIPT_REQUIRES) + \
            '\n' + options['packages']
        self.packages = filter(lambda v: v, map(
                lambda s: s.strip(), options['packages'].split('\n')))
        self.output_dir = options['output'].strip()
        self.domain = options.get('domain', 'silva').strip()
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        """Install the recipe.
        """
        scripts = []
        requirements, ws = self.egg.working_set()
        arguments = {'packages': self.packages,
                     'output_dir': self.output_dir,
                     'domain': self.domain}

        scripts.extend(
            zc.buildout.easy_install.scripts(
                [('%s-extract'% self.name,
                  'infrae.i18nextract.extract',
                  'egg_entry_point')],
                ws, self.options['executable'],
                self.buildout['buildout']['bin-directory'],
                arguments = arguments,
                ))

        return scripts

    update = install
