from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['requests','lxml']

setup(
    name="random_scraper",
    version="0.0.2",
    author="Malek Ben Sliman",
    author_email="mab2343@columbia.edu",
    description="Tools for Web-Scraping",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/random-scraper/random_scraper/",
    packages=find_packages(),
    scripts=['bin/random_scrape'],
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
