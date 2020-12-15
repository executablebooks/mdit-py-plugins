# from importlib import import_module
from os import path
import re
from setuptools import find_packages, setup


def get_version():
    text = open(
        path.join(path.dirname(__file__), "mdit_py_plugins", "__init__.py")
    ).read()
    match = re.compile(r"^__version__\s*\=\s*[\"\']([^\s\'\"]+)", re.M).search(text)
    return match.group(1)


setup(
    name="mdit-py-plugins",
    version=get_version(),
    description="Collection of plugins for markdown-it-py",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/executablebooks/mdit-py-plugins",
    author="Chris Sewell",
    author_email="chrisj_sewell@hotmail.com",
    license="MIT",
    packages=find_packages(exclude=["test*", "benchmarking"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="markdown lexer parser development",
    python_requires="~=3.6",
    install_requires=["markdown-it-py>=0.5.8,<2.0.0"],
    extras_require={
        "code_style": ["pre-commit==2.6"],
        "testing": [
            "coverage",
            "pytest>=3.6,<4",
            "pytest-cov",
            "pytest-regressions",
        ],
    },
    zip_safe=True,
)
