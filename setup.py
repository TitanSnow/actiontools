# Copyright (c) 2017 TitanSnow; All Rights Reserved


from setuptools import setup

setup(
    name = "actiontools",
    version = "0.0.0.dev0",
    packages = ["actiontools"],
    author = "TitanSnow",
    author_email = "tttnns1024@gmail.com",
    url = "https://github.com/TitanSnow/actiontools",
    entry_points = {
        "console_scripts": [
            "actiontools-storage = actiontools.cli:storage_main",
        ],
    },
    license = "Apache License Version 2.0"
)
