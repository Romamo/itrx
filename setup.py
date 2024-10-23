from setuptools import setup, find_packages

setup(
    name='itrx',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'backoff',
        'requests_ratelimiter'
    ],
    author='Roman Medvedev',
    author_email='github@romavm.dev',
    description='A client for interacting with the ITRX.io API',
    url='https://github.com/Romamo/itrx',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)