# -*- coding=utf-8 -*-
# The APACHE License (APACHE)
#
# Copyright (c) 2022 Author. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime
import os
import re

import PyPDF2

dir = "/home/uggla/Documents/Perso/Nounou"


class Paje:
    def __init__(self, dir, filter=""):
        self.dir = dir
        self.data = {}
        for pdf in sorted(self.search_pdf_file(filter)):
            print("Processing file: {}".format(pdf))
            date, salary = self.parse_text(self.extract_text(pdf))
            self.data[date] = salary

    def search_pdf_file(self, filter):
        pdf_files = []
        for root, dirs, files in os.walk(self.dir):
            for name in files:
                pdf_file = os.path.join(root, name)
                if re.search(filter, pdf_file) and pdf_file.endswith(".pdf"):
                    pdf_files.append(pdf_file)
        return pdf_files

    def extract_text(self, file):
        with open(file, "rb") as pdf_file:

            # creating a pdf reader object
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # creating a page object
            page = pdf_reader.getPage(0)

            # extracting text from page
            text = page.extractText()
            return text.split("\n")

    def parse_text(self, data):
        # __import__('pprint').pprint(data)
        end_date = ""
        raw_salary = ""
        for item in data:
            if "Période" in item:
                start_date = datetime.strptime(item.split(" ")[-3], "%d/%m/%Y")
                end_date = datetime.strptime(item.split(" ")[-1], "%d/%m/%Y")
            elif "Salaire brut" in item:
                raw_salary = float(item.split(" ")[-1].replace(",", "."))
            elif re.search(r"Salaire net \d+", item):
                net_salary = float(item.split(" ")[2].replace(",", "."))
            elif re.search(r"Salaire net déclaré \d+", item):
                net_salary = float(item.split(" ")[-1].replace(",", "."))
        return (
            end_date.strftime("%m/%Y"),
            {
                "raw_salary": raw_salary,
                "net_salary": net_salary,
                "start_date": start_date,
                "end_date": end_date,
            },
        )

    def display_salaries(self, type, reverse):
        sum = 0
        if type == "raw":
            salary_type = "raw_salary"
            sum = self.sum_raw_salaries()
        elif type == "net":
            salary_type = "net_salary"
            sum = self.sum_net_salaries()
        else:
            assert False

        for date, salary in sorted(
            self.data.items(),
            key=lambda item: item[1]["start_date"],
            reverse=reverse,
        ):
            print("{}: {}".format(date, salary[salary_type]))
        print("---------------------------------")
        print("Total {}: {}".format(type, sum))
        print("Total {}/80: {}".format(type, sum / 80))

    def sum_salaries(self):
        sum_raw = 0
        sum_net = 0
        for date, pay_sheet in self.data.items():
            sum_raw += pay_sheet["raw_salary"]
            sum_net += pay_sheet["net_salary"]
        return (sum_raw, sum_net)

    def sum_raw_salaries(self):
        raw, net = self.sum_salaries()
        return raw

    def sum_net_salaries(self):
        raw, net = self.sum_salaries()
        return net


paje = Paje(dir, r"20\d\d")
paje.display_salaries("net", True)
