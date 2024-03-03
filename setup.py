from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-expose-env",
    description="Datasette plugin to expose selected environment variables at /-/env for debugging",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-expose-env",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-expose-env/issues",
        "CI": "https://github.com/simonw/datasette-expose-env/actions",
        "Changelog": "https://github.com/simonw/datasette-expose-env/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_expose_env"],
    entry_points={"datasette": ["expose_env = datasette_expose_env"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "datasette-test"]},
    python_requires=">=3.8",
)
