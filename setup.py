"""
address_book
~~~~~~~~~~~~

address_book is a simple library for storing and querying data
about persons
"""

from setuptools import setup


setup(
    name='address_book',
    version='0.1.0',
    url='https://github.com/sanchopanca/address-book',
    license='MIT',
    author='Aleksandr Kovalev',
    author_email='aleksandr@kovalev.engineer',
    description='a simple library for storing and querying data about persons',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['address_book'],
)
