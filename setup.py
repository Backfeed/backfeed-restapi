import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    # 'pyramid',
    # 'pyramid_chameleon',
    # 'pyramid_debugtoolbar',
    # 'waitress',
    # 'cornice',
    # 'backfeed-protocol',
]

setup(
    name='backfeed-protocol-restapi',
    version='0.1',
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
    dependency_links=['http://github.com/Backfeed/backfeed-protocol-restapi/tarball/master'],
    tests_require=requires,
    test_suite="restapi",
    entry_points="""\
    [paste.app_factory]
    main = restapi:main
    """,
)
