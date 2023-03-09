import datetime
import pickle
from concurrent import futures
from random import shuffle
from typing import List

import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy_hunspell import spaCyHunSpell

DATA_DIR = "/mnt/sdb1/cds/"


def get_docs_from_text(nlp, text: str, slice_size: int, slicing_character: str):
    texts = []

    offset = 0
    docs = []
    try:
        index = text.index(slicing_character, slice_size)
    except ValueError:
        index = len(text)
    slice_text = text[offset: index]
    while len(slice_text) > 0:
        print(f"{offset} {index}")

        offset += len(slice_text)

        docs.append(nlp(slice_text))

        try:
            index = text.index(slicing_character, offset + slice_size)
        except ValueError:
            index = len(text)
        slice_text = text[offset: index]

    return docs


INPUT_FILES = [f"{DATA_DIR}data/extracted_processed_texts/AMZ_wmodel{i}_preprocessed.txt" for i in range(63, 83)]


def store_docs(input_files: List[str], model: str):
    nlp = spacy.load(model)

    def store_doc_for_one_book(input_file):
        print(f"process {input_file} {datetime.datetime.now()}")
        with open(input_file, "r") as file:
            text = file.read()

        docs = get_docs_from_text(nlp, text, 200000, "\n" )

        doc = Doc.from_docs(docs, False)

        with open(f"{DATA_DIR}data/entities_files/{input_file[-29:-17]}.dat", "wb") as file:
            pickle.dump(doc, file)

        print(f"{DATA_DIR}data/entities_files/{input_file[-29:-17]}.dat")

#    with futures.ThreadPoolExecutor(max_workers=4) as executor:
#        executor.map(store_doc_for_one_book, input_files)
    for file in input_files:
        store_doc_for_one_book(file)


store_docs(INPUT_FILES, "ner_training/ner_trained_model27_1/model-best")
