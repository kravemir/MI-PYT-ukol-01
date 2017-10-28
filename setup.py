from setuptools import setup

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='labelord_kravemir',
    version='0.2',
    description='CTU FIT - MI-PYT: homework labelord packaging',
    long_description=long_description,
    author='Miroslav Kravec',
    author_email='kravemir@fit.cvut.cz',
    license='Creative Commons Legal Code',
    url='https://github.com/kravemir/MI-PYT-ukol-01',
    py_modules=['labelord'],
    classifiers = [
        'Intended Audience :: Other Audience',
        'Framework :: Flask',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ]
)
