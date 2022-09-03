# -*- coding=utf-8 -*-
from datetime import datetime
import os
import re

import PyPDF2

file = "/home/uggla/Documents/Perso/Nounou/2017/09.pdf"
dir = "/home/uggla/Documents/Perso/Nounou"


class Paje():
    def __init__(self, dir, filter=""):
        self.dir = dir
        self.data = {}
        for pdf in sorted(self.search_pdf_file(filter)):
            print("Processing file: {}".format(pdf))
            date, salary = self.get_date_and_raw_salary(self.extract_text(pdf))
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
        with open(file, 'rb') as pdf_file:

            # creating a pdf reader object
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # creating a page object
            page = pdf_reader.getPage(0)

            # extracting text from page
            text = page.extractText()

            return text.split("\n")

    def get_date_and_raw_salary(self, data):
        date = ''
        salary = ''
        for item in data:
            if "Période" in item:
                date = datetime.strptime(item.split(" ")[-1], '%d/%m/%Y')
            elif "Salaire brut" in item:
                salary = float(item.split(" ")[-1].replace(",", "."))

        return (date, salary)

    def display(self):
        sum = self.sum_salaries()
        for date, salary in self.data.items():
            print("{}: {}".format(date.strftime("%Y-%m"), salary))
        print("---------------------------------")
        print("Total raw: {}".format(sum))
        print("Total raw/60: {}".format(sum/80))

    def sum_salaries(self):
        sum = 0
        for date, salary in self.data.items():
            sum += salary
        return sum


paje = Paje(dir, "2017")
paje.display()
