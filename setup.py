from distutils.core import setup

import packages

setup(name='YoukaiTools',
      version='0.1a',
      description='Python utilities library.',
      author='Nathaniel Caldwell',
      author_email='nbcwell@gmail.com',
      url='http://www.youkaicountry.com',
      #packages=['YoukaiTools', ],
      package_dir={'':'src'},
      packages=packages.getPackages()
      )

