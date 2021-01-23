from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ortisan_ta',
    version='1.0.0',
    packages=[''],
    url='https://github.com/tentativafc/ortisan_ta',
    license='',
    author='Marcelo Ortiz de Santana',
    author_email='tentativafc@gmail.com',
    description='This package contains a trade system by Marcelo. In development.',
    long_description=long_description,
    install_requires=[
     'MetaTrader5 >= 5.0.33',
     'numpy >= 1.19.3',     
     'pandas >= 1.1.4',
     'Rx >= 1.6.1',
     'scikit-learn >= 0.22.1'
    ],
)
