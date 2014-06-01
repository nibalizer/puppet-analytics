import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='puppet-analytics',
    version=0.1,
    long_description=__doc__,
    packages=['puppetanalytics'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)
