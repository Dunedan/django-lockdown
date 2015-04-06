from setuptools import setup, find_packages
import subprocess
import os.path

long_description = '\n'.join([open('README.rst').read(),
                              open('CHANGES.rst').read()])
setup(
    name='django-lockdown',
    version='1.1',
    description=('Lock down a Django site or individual views, with '
                 'configurable preview authorization'),
    long_description=long_description,
    author='Carl Meyer',
    author_email='carl@dirtcircle.com',
    url='https://github.com/Dunedan/django-lockdown/',
    packages=find_packages(),
    install_requires=['Django>=1.3'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    package_data={'lockdown': ['templates/lockdown/*.html',
                               'tests/templates/lockdown/*.html']},
)
