from setuptools import setup, find_packages

with open("README.md", "r",) as f: 
    long_description = f.read()

setup(
    name="pywgraph",
    version="0.0.1",
    description="A python implementation of weighted directed graphs",
    author="josek98",
    author_email="josemmsscc98@gmail.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
)
