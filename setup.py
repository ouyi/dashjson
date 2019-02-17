import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dashjson",
    version="0.1.5",
    author="Yi Ou",
    author_email="dashjson.project@gmail.com",
    description="A tool for exporting (or importing) Datadog dashboards to (or from) json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ouyi/dashjson",
    packages=setuptools.find_packages(),
    py_modules=['dashjson'],
    install_requires=['datadog>=0.26.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

