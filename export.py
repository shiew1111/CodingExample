import csv
import json
from exceptions import CoinExceptionAPI
from os import path


class ToFile:
    def __init__(self, data_format, closePriceList, file_name):
        self.file_name = file_name
        self.closePriceList = [
            {"date": close_price_dict["time_open"][:-10], "price": round(close_price_dict["close"], 2)}
            for close_price_dict in closePriceList]
        self.data_format = data_format
        self._file_name_check()
        self._check_if_file_exists()

    def export(self):
        if self.data_format.upper() == "CSV":
            self._export_csv()
        else:
            self._export_json()

    def _file_name_check(self):
        if "." in self.file_name:
            split_string = self.file_name.split(".", 1)
            if split_string[1].upper() == self.data_format.upper():
                pass

            elif split_string[1].upper() == "CSV" or split_string[1].upper() == "JSON":
                CoinExceptionAPI({"type": "File_formats_not_match"}).handle()
            else:
                print("Warning! You provided bad format in file_name, get rid of it.")
                self.file_name = split_string[0] + "." + self.data_format
        else:
            self.file_name += "." + self.data_format

    def _export_json(self):

        with open(self.file_name, 'w') as outfile:
            json.dump(self.closePriceList, outfile)

    def _export_csv(self):
        with open(self.file_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, self.closePriceList[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.closePriceList)

    def _check_if_file_exists(self):
        i = 1
        split_string = self.file_name.split(".", 1)

        while True:
            if not path.isfile(self.file_name):
                if i!=1:
                    print("File named like that, already exists. We change it to ", self.file_name)
                break
            self.file_name = split_string[0] + "_" + str(i) + "." + split_string[1]
            i += 1
