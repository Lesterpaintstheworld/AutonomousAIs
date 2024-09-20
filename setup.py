from setuptools import setup, find_packages

setup(
    name="kinos",
    version="0.51.1-dev",  # Updated to match __init__.py
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'kinos=kinos.main:main',  # Updated entry point
        ],
    },
)
