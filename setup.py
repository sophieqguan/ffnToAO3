import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffnToAO3",
    version="0.0.1",
    author="Clostone",
    author_email="cClostone@gmail.com",
    description="Transferring ffn works to AO3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clostone/ffnToAO3",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "ffnToAO3"},
    packages=setuptools.find_packages(where="ffnToAO3"),
    python_requires=">=3.6",
)