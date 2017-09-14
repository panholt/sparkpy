from distutils.core import setup

setup(
    name='sparkpy',
    author='Paul Anholt',
    author_email='panholt@gmail.com',
    version='0.1dev',
    packages=['sparkpy', 'sparkpy.models'],
    license='MIT',
    url='https://github.com/panholt/sparkpy',
    long_description=open('README.rst').read(),
    install_requires=['requests', 'requests-toolbelt']
)
