from distutils.core import setup

setup(
  name = 'marge',
  packages = ['marge'],
  package_dir = {'marge': 'marge'},
  package_data = {'marge': ['__init__.py', 'cleaner.py', 'config.py', 'config.yml', 'converter.py', 'enricher.py', 'enumerations.py', 'models.py', 'resolver.py', 'split.py', 'train.py', 'utils.py','configs/__init__.py', 'configs/first_pass.py', 'configs/second_pass.py', 'tests/__init__.py', 'tests/cleaner.py', 'tests/models.py', 'tests/utils.py']},
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
