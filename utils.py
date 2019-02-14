import json

import pandas as pd


class Json(object):

    def __init__(self):
        self.__reduced_item = {}

    @staticmethod
    def to_string(s):
        try:
            return str(s)
        except:
            return s.encode('utf-8')

    @staticmethod
    def merge_json(json_one, json_two):
        dict_a = json.loads(json_one)
        dict_b = json.loads(json_two)

        merged_dict = {key: value for (key, value) in (dict_a.items() + dict_b.items())}

        return json.dumps(merged_dict)

    def __reduce_item(self, key, value):

        if type(value) is list:
            i = 0
            for sub_item in value:
                self.__reduce_item(key + '_' + self.to_string(i), sub_item)
                i = i + 1

        elif type(value) is dict:
            sub_keys = value.keys()
            for sub_key in sub_keys:
                self.__reduce_item(key + '_' + self.to_string(sub_key), value[sub_key])

        else:
            self.__reduced_item[self.to_string(key)] = self.to_string(value)

    def convert_json_df(self, node, json_raw):

        try:
            data_to_be_processed = json_raw[node]
        except:
            data_to_be_processed = json_raw

        processed_data = []

        for item in data_to_be_processed:
            self.__reduced_item = {}
            self.__reduce_item(node, item)

            processed_data.append(self.__reduced_item)

        return pd.DataFrame(processed_data)
