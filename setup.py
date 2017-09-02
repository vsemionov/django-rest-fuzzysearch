from setuptools import setup, find_packages

setup(
    name='django-rest-fuzzysearch',

    version='0.10.0',

    description='Fuzzy Search for Django REST Framework',

    url='https://github.com/vsemionov/django-rest-fuzzysearch',

    author='Victor Semionov',
    author_email='vsemionov@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries',
    ],

    keywords='fuzzy search django rest python',

    packages=find_packages(),

    install_requires=[
        'Django>=1.11',
        'djangorestframework',
    ],
)
