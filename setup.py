from setuptools import setup, find_packages

setup(
    name="sgcm",
    version="0.1.1",
    description="A module for the SGC++ coding language!!!",
    author="Freakybob Team",
    author_email="freakybobsite@proton.me",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Freakybob-Team/SGCM",
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Homepage": "https://github.com/Freakybob-Team/SGCM",
        "Documentation": "https://github.com/Freakybob-Team/SGCM",
        "Repository": "https://github.com/Freakybob-Team/SGCM",
        "Issues": "https://github.com/Freakybob-Team/SGCM/issues",
    },
)
