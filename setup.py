
from setuptools import setup

"""
Description of how to make a python package
https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
"""


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='keepAlive',
      version='1.0.0',
      long_description=readme(),
      description='keepAlive in dontstarve',
      url='https://github.com/zhenglz/keepAlive',
      author='zhenglz',
      author_email='zhenglz@outlook.com',
      license='GPL-3.0',
      packages=[],
      install_requires=[
            'psutil',
      ],
      include_package_data=True,
      zip_safe=False,
)

