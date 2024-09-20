from setuptools import setup, find_packages

setup(
    name="kinos",  # Make sure this is lowercase
    version="0.1",
    packages=find_packages(),
    package_dir={'kinos': 'kinos'},  # Explicitly map the package to its directory
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'kinos=kinos.__main__:kinos_main',
        ],
    },
)