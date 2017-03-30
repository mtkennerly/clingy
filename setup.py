
from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

setup(
    name="clingy",
    version="1.0.0",
    description="A tool to save attachments from plain text emails",
    long_description=long_description,
    url="https://github.com/mtkennerly/clingy",
    author="Matthew T. Kennerly (mtkennerly)",
    author_email="mtkennerly@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Email",
        "Topic :: Utilities"
    ],
    keywords="email attachment",
    py_modules=["clingy"],
    extras_require={
        "dev": [
            "invoke",
            "tox"
        ]
    },
    entry_points={
        "console_scripts": [
            "clingy=clingy:main",
        ],
    }
)
