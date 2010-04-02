==================
infrae.i18nextract
==================

``infrae.i18nextract`` is a buildout recipe which create a script to
extract i18n strings from multiple packages into a ``.pot``.

The script support extraction from Python Script, Zope Page Template,
Chameleon Page Template, Formulator forms and Silva Metadata schemas.

Exemple in buildout::

  [silva-translation]
  recipe = infrae.i18nextract
  packages =
     silva.core.views
     silva.core.smi
  output = ${buildout:directory}
  domain = silva

