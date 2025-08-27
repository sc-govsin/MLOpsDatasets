from setuptools import setup, find_packages

def read_requirements():
    with open("./requirements.txt", encoding="utf-8") as f:
        return f.read().splitlines()

setup(
    name="MLOpsDatasets",
    use_scm_version=True,  # <-- version comes from git tags
    setup_requires=["setuptools-scm"],
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Govind Singh",
    author_email="govind.singh@scryai.com",
    description="A Python library to download datasets created with Scry.",
    long_description=open("README.MD", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sc-govsin/MLOpsDatasets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
