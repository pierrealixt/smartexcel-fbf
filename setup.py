import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SmartExcel",
    version="0.0.1",
    author="Pierre-Alix Tremblay",
    author_email="pierrealix@kartoza.com",
    description="A lib to create excel spreadsheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pierrealixt/SmartExcel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)