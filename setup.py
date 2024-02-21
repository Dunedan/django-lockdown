from setuptools import find_packages, setup

LONG_DESCRIPTION = '\n'.join([open('README.rst').read(),
                              open('CHANGES.rst').read()])

setup(
    name='django-lockdown',
    version='4.0.0',
    description=('Lock down a Django site or individual views, with '
                 'configurable preview authorization'),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Carl Meyer',
    author_email='carl@dirtcircle.com',
    maintainer='Daniel Roschka',
    maintainer_email='danielroschka@phoenitydawn.de',
    url='https://github.com/Dunedan/django-lockdown/',
    packages=find_packages(exclude=['lockdown.tests']),
    install_requires=['Django>=3.2', "python>=3.8"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    package_data={'lockdown': ['templates/lockdown/*.html']},
)
