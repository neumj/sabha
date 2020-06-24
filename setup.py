from setuptools import setup, find_packages

reqs = [
    "bokeh",
    "numpy",
    "pandas",
    "yaml"
]

conda_reqs = [
    "bokeh",
    "numpy",
    "pandas",
    "yaml"
]

test_pkgs = []

setup(
    name="sabha",
    python_requires='>3.4',
    description="Python package for routing through cost surfaces",
    url="https://github.com/neumj/sabha",
    install_requires=reqs,
    conda_install_requires=conda_reqs,
    test_requires=test_pkgs,
    packages=find_packages(),
    include_package_data=True
)
