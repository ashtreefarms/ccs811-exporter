#!/usr/bin/env python

import os
from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name="ccs811_exporter",
    version="0.0.1-alpha",
    author="Jake Krog",
    author_email="jake.krog@gmail.com",
    description="Prometheus exporter for the ams CCS811 sensor",
    long_description=README,
    license="MIT",
    keywords=["raspberry pi", "rpi", "prometheus", "CCS811", "i2c", "temperature", "eco2", "tvoc"],
    url="https://github.com/ashtreefarms/ccs811_exporter",
    download_url="https://github.com/ashtreefarms/ccs811_exporter/tarball/0.0.1-alpha",
    packages=find_packages(),
    install_requires=["Adafruit_CCS811", "prometheus_client"],
    entry_points={
        'console_scripts': [
            'ccs811_exporter = ccs811_exporter.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
    ]
)