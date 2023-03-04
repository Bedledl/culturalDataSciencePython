from _ast import List
from concurrent import futures
import datetime
import os
import tempfile
import threading
from typing import Tuple

import pytesseract
import cv2
import pdf2image
import numpy
from Levenshtein import ratio
from PyPDF2 import PdfFileReader
from os.path import isfile

pytesseract.pytesseract.tesseract_cmd = '/home/betti/culturalDataScience/venv/lib/tesseract/tesseract'
#PDF_DATA_DIR = "/home/betti/culturalDataScience/data/raw_pdfs/"
PDF_DATA_DIR = "/mnt/sdb1/cds/data/raw_pdfs/"
PDF_DATA_DIR_1_51 = "/mnt/sdb1/cds/data/raw_pdfs/raw_pdfs_99_48/"
EXTRACTED_FILES_DIR = "/mnt/sdb1/cds/data/extracted_texts_63_83/"

class Page:
    def __init__(self, pdf_path, page, label=None, numpy_array=None):
        self.__pdf_path = pdf_path
        self.__page = page
        self.label = label
        self.__numpy_array = numpy_array

#    def binarization_threshold(self):
#        ret, self.__cv2_binary = cv2.threshold(self.__cv2_binary, 127, 255, cv2.THRESH_BINARY)

    def generate_text_tesseract(self, dpi=400, language="deu") -> str:
        if self.__numpy_array is not None:
            numpy_arr = self.__numpy_array
        else:
            numpy_arr = self.get_numpy_array(dpi)
        img_rgb = cv2.cvtColor(numpy_arr, cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(img_rgb, lang=language)

    def get_numpy_array(self, dpi):
        if self.__numpy_array is not None:
            return self.__numpy_array

        images = pdf2image.convert_from_path(self.__pdf_path,
                                             dpi=dpi,
                                             first_page=self.__page,
                                             last_page=self.__page)

        return numpy.array(images[0])


class Book:
    def __init__(self, pdf_path, name):
        if not isfile(pdf_path):
            raise FileNotFoundError

        self.__pdf_path = pdf_path
        self.__name = name

        self.__pages = PdfFileReader(open(self.__pdf_path, 'rb')).numPages

    def __getitem__(self, page):
        if page <= self.pages:
            return Page(self.__pdf_path, page)
        else:
            raise ValueError(f"Page {page} does not exist in {self.__pdf_path}. It is only {self.__pages} pages long")

    @property
    def name(self):
        return self.__name

    @property
    def pages(self):
        return self.__pages

    def get_text_from_page(self, page_nr, dpi=400, language="deu"):
        p = Page(self.__pdf_path, page_nr)
        return p.generate_text_tesseract(dpi, language)

    def get_text_from_page_optimized(self, page_nr, dpi=93, language="deu"):
        p = Page(self.__pdf_path, page_nr)
#        p.binarization_threshold()
        return p.generate_text_tesseract(language)

    def get_text_from_pages(self, start, end, dpi=400, language="deu"):
        images = pdf2image.convert_from_path(self.__pdf_path,
                                             dpi=dpi,
                                             first_page=start,
                                             last_page=end-1)
        text = ""
        for image in images:
            p = Page(self.__pdf_path, 0, numpy_array=numpy.array(image))
            text += p.generate_text_tesseract(language=language)
        return text

    def get_numpy_array_from_page(self, page_nr, dpi, label):
        p = Page(self.__pdf_path, page_nr, )

    def print_fortschritt(self, printed: Tuple[bool], current_offset):
        first_quantil, second_quantil, third_quantil = 0.25 * self.pages, 0.5 * self.pages, 0.75 * self.pages
        if current_offset >= first_quantil and not printed[0]:
            print(f"{self.name}: 25%")
            printed[0] = True

        if current_offset >= second_quantil and not printed[1]:
            print(f"{self.name}: 50%")
            printed[1] = True

        if current_offset >= third_quantil and not printed[2]:
            print(f"{self.name}: 75%")
            printed[2] = True

    def get_text_from_whole_book(self, dpi, language):
        text = ""
        page_offset = 0
        printed_first, printed_second, printed_third = False, False, False
        while page_offset < self.pages:
            #self.print_fortschritt((printed_first, printed_second, printed_third), page_offset)
            text += self.get_text_from_pages(page_offset, page_offset + 25, dpi=dpi, language=language)
            page_offset += 25
        return text


def store_books(dpi=450, language="deu"):
    def store_booktest_in_file(book):
        print(f"Starting to read and store {book.name} at {datetime.datetime.now()} with {book.pages} Pages")

        textfile = open(EXTRACTED_FILES_DIR + book.name + ".txt", 'w')
        text = book.get_text_from_whole_book(dpi=dpi, language=language)
        textfile.write(text)

        textfile.close()
        print(f"Finished {book.name} at {datetime.datetime.now()}")

    amz_years_from_to = (70, 83)
    books = []

    for number in range(*amz_years_from_to):
        b = Book(PDF_DATA_DIR + f"amzband{number}.pdf", f"AMZ_wmodel{number}")
        books.append(b)

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(store_booktest_in_file, books)


def compare_trainings_models():
    b = Book(f"/home/betti/culturalDataScience/data/allmuszeitungband1799google.pdf", f"AMZ1799")
    os.environ.update({"TESSDATA_PREFIX": "/home/betti/culturalDataScience/venv/lib/tessdata_best"})
    print("Generating page with first model:")
    text1 = b.get_text_from_page(22)
    os.environ.update({"TESSDATA_PREFIX": "/home/betti/culturalDataScience/venv/lib/tesstrain/data"})
    print("Generating page with second model:")
    text2 = b.get_text_from_page(22)
    for line1, line2 in zip(text1, text2):
        if line1 == line2:
            continue
        else:
            print("Unterschiedliche Zeilen:")
            print(line1)
            print(line2)


def get_test_page(dpi=93, language="deu"):
    b = Book(PDF_DATA_DIR_1_51 + f"amzband1.pdf", f"AMZ1")
    print("Generating page :")
    return b.get_text_from_page(203, dpi, language)


def get_test_pages(dpi=93, language="deu"):
    b = Book(PDF_DATA_DIR + f"amzband1.pdf", f"AMZ1")
    print("Generating page :")
    return b.get_text_from_pages(22, 72, dpi, language)


def print_test_page(dpi=93, language="deu"):
    print(get_test_page(dpi, language))


def compare_two_mlmodels_for_text():
    text1 = get_test_page(400, language="deu").split("\n")
    #text1 = get_test_page(400, language="amz-trained").split("\n")
    text2 = get_test_page(400, language="amz-trained2")
    print(text2)
    text2 = get_test_page(400, language="amz-trained2").split("\n")

    print(text1)
    print("text2:")
    print(text2)
    print("tex finish")

    max_line_len = max([len(line) for line in text1 + text2]) + 1

    for l1, l2 in zip(text1, text2):
        fill_up1 = int(max_line_len - len(l1))*' '
        fill_up2 = int(max_line_len - len(l2))*' '
        print(l1 + fill_up1 + l2 + fill_up2)

#compare_two_mlmodels_for_text()
store_books(dpi=400, language="amz-weisthuemer-combined")


def try_test_model(model: str):
    text = get_test_page(400, language=model)
    with open("data/check_data/check_text.txt", "r") as file:
        check_text = file.read()

    return ratio(text, check_text)

#print(f"deu modell: {test_model('deu')}")
#print(f"amztrained2 modell: {test_model('amz-trained2')}")
#print(f"amztrained modell: {test_model('amz-trained')}")
#print(f"first modell: {test_model('first-test')}")
#print(f"second modell: {test_model('second-test')}")
#print(f"weistuemer erster versucht: {test_model('weisthuemer1_2_added')}")
#print(f"weisthuemer auf deu: {test_model('weisthuemer1_2_new')}")
#print(f"amz-weisthuemer-combined: {try_test_model('amz-weisthuemer-combined')}")


#print(get_test_page(400, language='amz-weisthuemer-combined'))


# weisthuemer1-2 added: erster versucht weisthumer auf amz-trained zu adden
#amztrained ist das beste aus deu amztrained, maztrained2, first und second test
# weisthuemer 1-2 new: weisthuemer auf deu
#weisthuemer_amz: amz gt auf weisthiemer 1-2 new
