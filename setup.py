import os
from setuptools import setup, find_packages

# Load long_description from README.rst
readme = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(readme, 'rU').read().decode('utf8')

# Construct version string
from heightfield import __version__
version = '.'.join([str(component) for component in __version__])

setup(
    name='heightfield',
    version=version,
    packages=find_packages(),
    package_data={
        'heightfield': ['data/*.png'],
    },
    description=u"Generate random maps by particle deposition",
    long_description=long_description,
    author='Daniel Pope / Reading Python Dojo',
    author_email='lord.mauve@gmail.com',
    url='https://bitbucket.org/lordmauve/heightfield',
    install_requires=[
        'PIL>=1.1.6',
    ],
    license='LGPL',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics',
    ],
    entry_points={
        'console_scripts': [
            'heightfield = heightfield.main:main',
        ]
    }
)
