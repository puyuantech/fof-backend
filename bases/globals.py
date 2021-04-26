from flask_sqlalchemy import SQLAlchemy
from configs import Configurator, DEFAULT_CONFIG_PATH
from surfing.util.config import SurfingConfigurator
from flask_caching import Cache
from celery import Celery
from extensions.cas.cas_base import FlaskCas


cache = Cache()
celery = Celery()
db = SQLAlchemy()
cas = FlaskCas()
settings = Configurator().from_py_file(DEFAULT_CONFIG_PATH)
SurfingConfigurator(settings['SURFING_CONFIG'])
