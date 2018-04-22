import os

from pip._internal.req import parse_requirements
from setuptools import setup, find_packages
from distutils.util import convert_path

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# ========================================
# Parse requirements for all configuration
# ========================================
install_reqs = parse_requirements(filename=os.path.join('.', 'requirements.txt'), session='update')
reqs = [str(ir.req) for ir in install_reqs]

# ========================================
# Readme
# ========================================
with open(os.path.join('.', 'README.md')) as readme:
    README = readme.read()

# ========================================
# Version parsing
# ========================================
main_ns = {}
ver_path = convert_path('muadib/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='kryten-worksheet',
    version=main_ns['__version__'],
    packages=find_packages(),
    include_package_data=True,
    author='lordoftheflies',
    author_email='laszlo.hegedus@cherubits.hu',
    license='Apache 2.0 License',  # example license
    description='Crawler application for scraping single page apps.',
    long_description=README,
    url='https://github.com/lordoftheflies/muadib-notebook/',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Monitoring',
        'Development Status :: 2 - Pre-Alpha'
    ],
    install_requires=reqs,
    dependency_links=[
        'https://jenkins:qwe123@pypi.cherubits.hu'
    ],
    entry_points={},
)