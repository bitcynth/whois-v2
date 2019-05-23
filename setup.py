import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='whois-v2',
    version='0.0.4',
    author='Cynthia Revstrom',
    author_email='me@cynthia.re',
    description='A web based WHOIS client and parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bitcynth/whois-v2',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'Flask'
    ],
    include_package_data=True
)