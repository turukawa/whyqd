import os
from setuptools import find_packages, setup

print os.path.dirname('__file__')
print os.path.join(os.path.dirname('__file__'), 'README.rst')

with open(os.path.join(os.path.dirname('__file__'), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath('__file__'), os.pardir)))

# Info from http://stackoverflow.com/a/11669299

setup(
    name='whyqd',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU Affero General Public License',
    description='Whyqd is an extensible object-based wiki bringing revision control, content presentation, branching and embedding to any type of digital object.',
    long_description=README,
    url='https://github.com/turukawa/whyqd',
    author='Gavin Chait',
    author_email='gchait@whythawk.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)