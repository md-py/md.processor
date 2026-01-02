import setuptools


with open('readme.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='md.processor',
    version='1.1.0',
    description='Common task processing contracts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='License :: OSI Approved :: MIT License',
    url='https://github.com/md-py/md.processor',
    package_dir={'': 'lib/'},
    packages=['md.processor'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
