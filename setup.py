from setuptools import setup

setup(name='chaotic_maps',
      version='0.1',
      description='Easily create cobweb plots and bifurcations diagrams for one-dimensional maps.',
      url='http://github.com/eowagner/chaotic_maps',
      author='Elliott Wagner',
      author_email='e.o.wagner@gmail.com',
      license='MIT',
      packages=['chaotic_maps'],
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib'
          ],
      zip_safe=False)
