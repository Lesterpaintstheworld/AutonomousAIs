from setuptools import setup, find_packages

setup(
    name="kinos",
    version="0.51.1-dev",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "aiohappyeyeballs==2.4.0",
        "aiohttp==3.10.5",
        "Flask==3.0.3",
        "gevent==24.2.1",
        "gunicorn==23.0.0",
        "requests==2.32.3",
        "streamlit==1.38.0",
    ],
    entry_points={
        'console_scripts': [
            'kinos=kinos.main:main',
        ],
    },
)
