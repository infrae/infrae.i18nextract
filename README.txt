==================
infrae.i18nextract
==================

``infrae.i18nextract`` is a buildout recipe which create a script to
extract i18n strings from multiple packages into a ``.pot``. A script
to merge  or compile all available translations is also available.

The script support extraction from Python Script, Zope Page Template,
Chameleon Page Template, Formulator forms and Silva Metadata schemas.

Exemple in buildout::

  [silva-translation]
  recipe = infrae.i18nextract
  packages =
     silva.core.views
     silva.core.smi
  output = ${buildout:directory}
  output-package = silva.translations
  domain = silva
  extra-paths = ${zope2:location}/lib/python


Options
=======

`packages`
   List of packages to extract translation from.

`output`
   Output directory for the created template file.

`output-package`
   If specified, you will be able to create the template file directly
   inside that package.

`domain`
   Translation domain to use.

`extra-paths`
   Extra python path to add in order to able to load the Python code
   to extract translations strings from it.

Scripts
=======

Two scripts are created:

`part-name-extract`
   That do extract the translations. The option `-p` saves the created
   template file in the `output-package` specified in the buildout part.

`part-name-manage`
   Manage translation files in the `output-package` specified in the
   buildout part:

   - `-m` merge the translation template file into all existing
     translations files.

   - `-c` compile all existing translations files.

The last script requires to have the commands `msgfmt` and `msgmerge`
installed on the system (available in gettext).

