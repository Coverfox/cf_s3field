from setuptools import setup

try:
    long_description = open("README.rst").read()
    long_description += open('ChangeLog.rst', 'rt').read()
except:
    long_description = ""

setup(
    name="cf_s3field",
    description="S3 fields to upload images to s3 instead of file system",
    long_description=long_description,
    version="0.0.3",
    author="Hitul Mistry", 
    maintainer="",
    maintainer_email="",
    url="",
    licence="",
    install_requires=[
        "Django>=1.7", "boto"
    ],
    packages=["cf_s3field"], 
    zip_safe=True,
    keywords=['Django', 's3field', 'coverfox', 'cf_s3_field'],
    classifiers=[
     'Development Status :: stable',

        'Intended Audience :: Developers',

        'Natural Language :: English',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development',
    ],
)
