==================
infrae.i18nextract
==================

``infrae.i18nextract`` is a buildout recipe which create a script to
extract i18n strings from multiple packages into a ``.pot``. A script
to merge all available translations is also available.

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
