import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffnToAO3",
    version="0.1.2",
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
    package_dir={"": "src"},
    include_package_data=True,
    package=setuptools.findall("src"),
    py_modules=['ffnToAO3.example', 'ffnToAO3.get_ffn', 'ffnToAO3.ratings', 'ffnToAO3.unix', 'ffnToAO3.uploadAO3'],
    python_requires=">=3.6",
)