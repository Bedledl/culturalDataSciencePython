import random
import re

import spacy as s
from spacy.tokens import Doc, Span, DocBin
from spacy.cli.train import train

from Composer import Composer
from create_ner_testdata import create_ner_testdata

DATA_DIRECTORY = "/mnt/sdb1/cds/data/"
# https://github.com/explosion/spaCy/blob/v2.3.x/examples/training/train_ner.py

composer_list = [
    Composer("Ludwig van", "Beethoven", 1900, 1900),
    Composer("Wolfgang Amadeus", "Mozart", 1900, 1900),
    Composer("Hans", "Köhler", 1900, 1900),
    Composer("Leo", "Wranitaky", 1900, 1900),
    Composer("Antonio", "Romberg", 1900, 1900),
    Composer("Theodor", "Haydn", 1900, 1900)
]

testfiles_ner = [f"{DATA_DIRECTORY}ner_checkdata/ner_test_ents_{i}" for i in range(1, 8)]


def get_testdata_doc(nlp, testdata_annotated: str):
    with open(testdata_annotated, "r") as test_ner:
        test_text_annotated = test_ner.read()

    test_text = re.sub("#", "", test_text_annotated)

    testdata = create_ner_testdata(testdata_annotated)

    # optimizer = nlp.initialize()
    doc = nlp(test_text)
    ents = []
    for begin, end in testdata:
        print(test_text[begin:end])
        ss = doc.char_span(begin, end, label="PER")
        if not ss:
            pass
        else:
            ents.append(ss)

    doc_ents = [ent for ent in doc.ents if ent.label_ != "PER"]
    doc.ents = ents
    for e in doc_ents:
        try:
            doc.ents = list(doc.ents) + [e]
        except ValueError:
            continue

    return doc


def train_ner_model(testfiles, output_spacy):
    nlp = s.load("de_core_news_lg")

    db = DocBin()

    for path in testfiles:
        doc = get_testdata_doc(nlp, path)
        db.add(doc)

    db.to_disk(output_spacy)

    train("ner_training/config.cfg",
          overrides={"paths.train": output_spacy, "paths.dev": output_spacy},
          output_path="ner_training/ner_trained_model27_1")


def test_ner_model(model_path, text_path):
    with open(text_path) as textfile:
        text = textfile.read()

    spans = create_ner_testdata(f"{DATA_DIRECTORY}ner_checkdata/check_ner_text_ents.txt")
    check_names = [text[begin:end] for begin, end in spans]
    print(check_names)

    nlp_trained = s.load(model_path)
    nlp_de = s.load("de_core_news_lg")

    doc_trained = nlp_trained(text)
    doc_de = nlp_de(text)
    print([e.text for e in doc_trained.ents if e.label_ == "PER"])
    print([e.text for e in doc_de.ents if e.label_ == "PER"])


train_ner_model(testfiles_ner, f"{DATA_DIRECTORY}ner_checkdata/ner_trained_mult_28_1_de_source.spacy")

#test_ner_model("ner_training/ner_trained_model27_1/model-best", "data/ner_checkdata/check_ner_text.txt")
#print("model last:")
#test_ner_model("ner_training/ner_trained_model27_1/model-last", "data/ner_checkdata/check_ner_text.txt")
