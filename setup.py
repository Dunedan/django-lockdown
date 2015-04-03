from setuptools import setup, find_packages
import subprocess
import os.path

long_description = '\n'.join([open('README.rst').read(),
                              open('CHANGES.rst').read(),
                              open('TODO.rst').read()])
setup(
    name='django-lockdown',
    version='0.1.3',
    description=('Site-wide or per-view lockdown with customizable preview '
                 'authorization'),
    long_description=long_description,
    author='Carl Meyer',
    author_email='carl@dirtcircle.com',
    url='http://bitbucket.org/carljm/django-lockdown/',
    packages=find_packages(),
    install_requires=['Django>=1.3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    package_data={'lockdown': ['templates/lockdown/*.html',
                               'tests/templates/lockdown/*.html']},
)
