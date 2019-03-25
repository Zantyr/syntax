from setuptools import setup

setup(name='syntax',
      version='0.1',
      description='Simple utilities to extend the language',
      url='http://github.com/Zantyr/syntax',
      author='Zantyr',
      author_email='tomasik.kwidzyn@gmail.com',
      license='MIT',
      install_requires=[
          'gitpython',
      ],
      packages=['syntax'],
      zip_safe=False)
