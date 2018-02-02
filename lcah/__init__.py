from logging import DEBUG
from os.path import dirname
from pathlib import Path

from flask import Flask
import pymongo

directory = dirname(__file__)
app = Flask("LCAH",
            template_folder=Path(f"{directory}/templates"),
            static_folder=Path(f"{directory}/static"))
mongo = pymongo.MongoClient()

app.logger.setLevel(DEBUG)

import lcah.views
