from setuptools import setup

packages=['dvidsync']

setup(name='dvidsync',
      version='0.1',
      description='Enable syncing between two dvid servers',
      url='https://github.com/janelia-flyem/dvidsync',
      packages=packages,
      entry_points={
          'console_scripts': [
              'dvidsync = dvidsync.__main__:main'
          ]
      },
      )
