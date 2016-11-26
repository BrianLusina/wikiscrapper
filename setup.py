try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

setup(
    name="WikiScraper",
    author="Brian Lusina",
    version="1.0.0",
    author_email="lusinabrian@gmail.com",
    description="Wikipedia scrapper to fetch top 20 most sought words",
    long_description=open("README.md").read(),
    install_requires=["nose", "beautifulsoup4", "lxml", "requests", "tabulate", "stop-words",
                      "pytest", "py"],
    scripts=[],
    packages=['wikiscraper', "tests"],
    license="",
    url="",
    requires=["requests"],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Development",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ]
)
