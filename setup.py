import os
from setuptools import setup, find_packages

from django_zipfile import VERSION

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = ['django']

setup(
    name = "django-zipfile",
    version = ".".join(map(str, VERSION)),
    description = "A ZipFile subclass that accepts Django Templates",
    long_description = read('README.rst'),
    url = 'https://github.com/fcurella/django-zipfile',
    license = 'MIT',
    author = 'Flavio Curella',
    author_email = 'flavio.curella@gmail.com',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = requirements,
)
