import setuptools

setuptools.setup(
    name="ppc",
    version="0.0.1",
    author="Valyrie Jacqueline Heather Autumn",
    author_email="jaculusgal@gmail.com",
    description="python parser combinator framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={""},
    packages=setuptools.find_packages(where="ppc"),
    python_requires=">=3.6",
)