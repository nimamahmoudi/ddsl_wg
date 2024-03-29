import setuptools
import re
import os
import ast

# parse version from locust/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_init_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ddsl_wg", "__init__.py")
with open(_init_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setuptools.setup(
    name="ddsl_wg",
    version=version,
    url="https://github.com/nimamahmoudi/ddsl_wg",
    author="Nima Mahmoudi",
    author_email="nima_mahmoudi@live.com",
    description="A workload generator made in DDSL lab of University of Alberta.",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=['numpy>=1.16.4', 'boto3>=1.9.170', 'pandas>=0.24.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={},

)

