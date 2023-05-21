#encoding=utf-8
import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="flow_control", # Replace with your own username
    version="2.0.0",
    author="liuyancong",
    author_email="1437255447@qq.com",
    description="A flow control packages,control QPS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mt6979/flow_control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
