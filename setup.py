import os
from setuptools import setup, find_packages

# Load long_description from README.rst
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme, 'rU').read().decode('utf8')

setup(
    name='heightfield',
    version="0.1",
    packages=find_packages(),
    description=u"Generate random maps by particle deposition",
    long_description=long_description,
    author='Daniel Pope / Reading Python Dojo',
    author_email='lord.mauve@gmail.com',
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
    package_data={
        'heightfield': ['data/*.png'],
    },
    entry_points={
        'console_scripts': [
            'heightfield = heightfield.main:main',
        ]
    }
)
