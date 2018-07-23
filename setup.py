from distutils.core import setup

setup(
    name='TimeAndMoney',
    version='0.1',
    author='Ilya Gotfryd',
    author_email='ilya.gotfryd@gmail.com',
    packages=['timeandmoney'],
    license='LICENSE.txt',
    description='port of time and money Java librarty',
    long_description=open('README.md').read(),
    install_requires=[
       "pytz"
    ]
)
