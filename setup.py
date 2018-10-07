
from setuptools import setup, find_packages

requires = [
    'aiosqlite',
    'tornado',
    'tornado-sqlalchemy',
    ]

setup(name='owm_cities',
      version='1.0.0',
      description='Unofficial api for OWM cities',
      author='McWladkoE',
      author_email='svevladislav@gmail.com',
      url='',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      initialize_owm_cities_db = owm_cities.initialize_db:main
      run_owm_cities_server = owm_cities.server:main
      """,
      )
