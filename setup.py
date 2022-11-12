from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

with open('version.txt', "r", encoding="utf-8") as f:
    version = f.read().strip()

setup(
    name="podaac-cloud-notification-message-schema",
    version=version,
    description="PO.DAAC Cloud Notification Message Schema",
    url='https://github.com/podaac/cloud-notification-message-schema',
    author='PO.DAAC',
    author_email='podaac@podaac.jpl.nasa.gov',
    install_requires=[
    ],
    extras_require={
        'testing': [
            'pytest==5.3.5'
        ]
    },
    packages=['.'],
    package_data={
       'samples': ['*.json']
    },
    include_package_data=True
)