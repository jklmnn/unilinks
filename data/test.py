#!/usr/bin/python3

import unittest
import json
import validators
import ddt
from jsonschema import validate

indexschema = {
                "title":"JSon schema for index file.",
                "type":"array",
                "items":{
                        "type":"object",
                        "properties":{
                                "id":{
                                        "type":"string"
                                        },
                                "title":{
                                        "type":"string"
                                        }
                                },
                        "required":["id", "title"]
                        }
                }

subschema = {
                "title":"JSon schema for subjects.",
                "type":"array",
                "items":{
                        "type":"object",
                        "properties":{
                                "title":{
                                        "type":"string",
                                        },
                                "entries":{
                                        "type":"array",
                                        "items":{
                                                "type":"object",
                                                "properties":{
                                                        "name":{
                                                                "type":"string"
                                                                },
                                                        "url":{
                                                                "type":"string"
                                                                }
                                                        },
                                                "required":["name", "url"]
                                                }
                                        }
                                },
                        "required":["title", "entries"]
                        }
                }

def load_files():
        jf = open("index.json", "r")
        files = [_id['id'] for _id in json.load(jf)]
        jf.close()
        return files

def load_links(files):
        entries = []
        for sfile in files:
                with open("{0}.json".format(sfile)) as f:
                        data = json.load(f)
                        for semester in data:
                                entries.extend(semester["entries"])
        return entries

@ddt.ddt
class JsonValidate(unittest.TestCase):

        def test_index(self):
                with open("index.json", "r") as f:
                        data = json.load(f)
                validate(data, indexschema)

        @ddt.data(*load_files())
        def test_files(self, value):
                with open("{0}.json".format(value), "r") as f:
                        data = json.load(f)
                validate(data, subschema)

        @ddt.data(*load_links(load_files()))
        def test_links(self, entry):
                if entry["url"]:
                        status = validators.url(entry["url"])
                        self.assertTrue(status == True,
                                "Test failed for\nSite: {0} \nURL: {1}\nResult: {2}".format(
                                    entry["name"], entry["url"], "True" if status else status.value))

