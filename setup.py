import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SmartExcel",
    version="1.0.0",
    author="Pierre-Alix Tremblay @ Kartoza",
    author_email="pierrealix@kartoza.com",
    description="A lib to generate Excel spreadsheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kartoza/smartexcel-fbf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)