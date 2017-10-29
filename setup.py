from setuptools import setup

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='labelord_kravemir',
    version='0.3',
    description='CTU FIT - MI-PYT: homework labelord packaging',
    long_description=long_description,
    author='Miroslav Kravec',
    author_email='kravemir@fit.cvut.cz',
    keywords='homework,fit ctu,mi-pyt',
    license='Creative Commons Legal Code',
    url='https://github.com/kravemir/MI-PYT-ukol-01',
    packages=['labelord'],
    package_data={
        'labelord' : ['templates/*.html'],
    },
    classifiers = [
        'Intended Audience :: Other Audience',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires = [
        'Flask>=0.12',
        'click>=6.7',
        'configparser>=3.5.0',
        'requests>=2.0'
    ],
    entry_points={
        'console_scripts': [
            'labelord = labelord.labelord:main',
        ],
    },
    zip_safe=False
)
