from django.test import TestCase
import pymongo
# Create your tests here.
conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "127.0.0.1", "27017", "admin"))