from setuptools import setup, find_packages

setup(
    name="aider",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "discord",
        "python-telegram-bot",
        "playwright",
        # Add any other dependencies your project needs
    ],
    entry_points={
        'console_scripts': [
            'aider=aider.__main__:main',
        ],
    },
)