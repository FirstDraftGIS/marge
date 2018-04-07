from distutils.core import setup

setup(
  name = 'marge',
  packages = ['marge'],
  package_dir = {'marge': 'marge'},
  package_data = {'marge': ['__init__.py']},
  version = '0.1',
  description = 'Model that Automatically Resolves Geographic Entities',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/marge',
  download_url = 'https://github.com/DanielJDufour/marge/tarball/download',
  keywords = ['location','geo','python','tensorflow'],
  classifiers = [],
  install_requires=["numpy", "pandas", "scipy"]
)
