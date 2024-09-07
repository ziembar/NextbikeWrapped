from neo4j import GraphDatabase
from neomodel import (config, StructuredNode, StringProperty, Relationship, FloatProperty, IntegerProperty, StructuredRel)
from decouple import config as env_config
from pymongo.mongo_client import MongoClient
from collections.abc import MutableMapping


uri = env_config('NEO4J_URI')
auth = (env_config('NEO4J_USERNAME'), env_config('NEO4J_PASSWORD'))
driver = GraphDatabase.driver(uri, auth=auth)

config.DRIVER = driver

uri_mongo = env_config('MONGODB_URI')
mongo_client = MongoClient(uri_mongo)


def getMongoClient():
    return mongo_client

def getDriver():
    return driver

class Station(StructuredNode):
    name = StringProperty()
    uid = IntegerProperty(unique_index=True)
    city_id = IntegerProperty(index=True)
    lat = FloatProperty(index=True)
    lng = FloatProperty(index=True)

    stations = Relationship('Station', 'PATH')


class Path(StructuredRel):
    distance = IntegerProperty()
    time = IntegerProperty()
