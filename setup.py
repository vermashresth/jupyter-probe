from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="jupyter-probe",
    version="0.1.2",
    author="Shresth Verma",
    author_email="vermashresth@gmail.com",
    description="A package to monitor, manage, declare and analyse notebook resource usage on jupyter environments",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/vermashresth/jupyter-probe",
    packages=find_packages(),
    install_requires=[
    'pandas',
    'psutil',
    'requests',
    'py3nvml',
    'rich',
    'jupyter',
    'jupyterlab',
    'filelock'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
