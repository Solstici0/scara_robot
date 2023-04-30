# encoding: utf8
from setuptools import setup

def read_requirements():
    requirements = []
    with open("./requirements.txt") as f:
        for req in f:
            req = req.replace("\n", " ")
            requirements.append(req)
    return requirements


def read_description():
    with open("README.md", "r") as f:
        descr = f.read()
    return descr

setup(
    name='scara',
    version='0.0.1',
    description='Solsticios Selective Compliance Articulated Robot Arm package',
    long_description=read_description(),
    long_description_content_type="text/md",
    packages=["scara"],
    install_requires=read_requirements(),
    author='Solsticio',
    author_email='contacto@solstic.io',
    url='https://github.com/Solstici0/scara',
    license_files=('LICENSE.txt',),

)
