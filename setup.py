import os

from setuptools import setup, find_packages
import restapi

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

version = restapi.__version__

requires = [
    'webtest',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'cornice',
    'backfeed-protocol',
    'BeautifulSoup4',
]

setup(
    name='backfeed-protocol-restapi',
    version=version,
    description='restapi',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="restapi",
    entry_points="""\
    [paste.app_factory]
    main = restapi:main
    """,
)
