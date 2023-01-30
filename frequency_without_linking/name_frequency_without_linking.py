# für entity linking könnte man die Entitiy Linking Komponente von Spacy benutzen, dafür müssteich aber eine schon fertige
# KB schreiben. Ich will aber, dass auch z.b. unbekannte Künstler erkannt werden.
# deshalb erstelle ich den suchbaum selber
# Nachnamen ->* Name ->* Vorname
# Im Grunde bilden wir einen Suchbaum für Namen und speichern dort auch die Vorkommen ab
# Es gibt eine Nachnameninstanz für jeden Nachnamen
# für jede Person gibt es dann eine Nameninstanz mit den Informationen über den Namen
# jedem Nachnamen werden also Personen mit sicheren Vornamen zugeordnet und eine Nameninstanz mit leeren Vornamen
# es kann sein, dass die Vornamen nur abgekürzt bekannt sind. Wenn die namen ausgeschrieben bekannt werden,
# kann diese Information dann aktualisiert werden
# in den Namen werden dann die Funde gespeichert
import csv
import pickle
import re
from typing import List, Tuple, Dict

anreden = ["Mad.", "Herr", "Hr.", "Hrn.", "Dem.", "Madame", "Madamoiselle",
           "Demoiselle", "Frau", "Herrn", "Fräulein", "Miss"]
funktion = ["Kapellmeister", "Kapellm.", "Organist", "Kammermusikus", "Musikdirector", "Musikdireetor"]

REGEX_NACHNAME = "(?P<nachname>[^(\W|\d|_)]*)"
REGEX_ANREDEN = f"(({'|'.join(anreden)})\s?)"
REGEX_FUNKTION = f"(({'|'.join(funktion)})\s?)"
REGEX_VORNAME_ABKÜRZUNG = "([^(\W|\d|_)]{1,2}\.?)"
REGEX_VORNAME = "([^(\W|\d|_)]*)"
REGEX_VORNAMEN = f"(?P<vornamen>({REGEX_VORNAME_ABKÜRZUNG}\s?|{REGEX_VORNAME}\s){{0,3}}?)"
REGEX_VORNAMEN_NACHGESTELLT = f"(?P<vornamen>(({REGEX_VORNAME_ABKÜRZUNG}\s?){{0,3}}|({REGEX_VORNAME}?(\s{REGEX_VORNAME}){{0,2}})))"


match_patterns = [
    # "Hr. W. A. Mozart"
    re.compile(f"{REGEX_ANREDEN}?{REGEX_FUNKTION}?{REGEX_VORNAMEN}{REGEX_NACHNAME}"),
    # "Hr. Mozart
    re.compile(f"{REGEX_NACHNAME},\s??{REGEX_VORNAMEN_NACHGESTELLT}")
]


class Vorkommen:
    def __init__(self, buch_name: str, file_name: str, year: int, begin_char: int, end_char: int,
                 text: str, nachname: str, vornamen: str):
        self.buch_name = buch_name
        self.file_name = file_name
        self.year = year
        self.begin_char = begin_char
        self.end_char = end_char
        self.text = text
        self.nachname = nachname
        self.vornamen = vornamen


class Vorname:
    '''
    Ein Vorname also z.B. "Wolfgang", oder auch "W" mit abkürzung=True
    '''
    def __init__(self, vorname: str, abgekürzt: False):
        self.abgekürzt = abgekürzt
        self.vorname = vorname


def split_up_vornamen(vornamen_str: str) -> List[Vorname]:
    vornamen = []

    vornamen_str_split = vornamen_str.split()
    for vorname in vornamen_str_split:
        if re.fullmatch(REGEX_VORNAME_ABKÜRZUNG, vorname):
            vornamen.append(Vorname(vorname.strip('.'), abgekürzt=True))
        elif re.fullmatch(REGEX_VORNAME, vorname):
            vornamen.append(Vorname(vorname, abgekürzt=False))
    return vornamen


class Name:
    def __init__(self, nachname: str, vornamen: List[Vorname], nachname_obj):
        self.nachname = nachname
        self.vornamen = vornamen
        self.nachname_obj = nachname_obj
        self.vorkommen = {}
        print("added new person: ", str(self))

    def add_vorkommen(self, vorkommen: Vorkommen):
        if vorkommen.year in self.vorkommen.keys():
            self.vorkommen[vorkommen.year].append(vorkommen)
        else:
            self.vorkommen[vorkommen.year] = [vorkommen]
        self.nachname_obj.increment_frequenz()

    def match(self, vornamen: List[Vorname]) -> bool:
        if len(vornamen) != len(self.vornamen):
            return False

        for vn1, vn2 in zip(vornamen, self.vornamen):
            if vn1.vorname == vn2.vorname:
                continue
            if vn1.abgekürzt and vn2.vorname.startswith(vn1.vorname):
                continue
            if vn2.abgekürzt and vn1.vorname.startswith(vn2.vorname):
                continue
            return False

        return True

    def may_complete_vornamen(self, vornamen: List[Vorname]):
        # only execture if vornamen are matching!
        if not self.match(vornamen):
            return

        for vn1, vn2 in zip(vornamen, self.vornamen):
            if vn2.abgekürzt and not vn1.abgekürzt:
                vn2.vorname = vn1.vorname
                vn2.abgekürzt = False

    def __str__(self):
        return f"{' '.join([v.vorname for v in self.vornamen])} {self.nachname}"


class Nachname:
    def __init__(self, nachname: str):
        self.nachname = nachname
        self.name_instanzen = []
        self.empty_instance = Name(self.nachname, [], self)
        self.frequenz = 0

    def increment_frequenz(self):
        if self.frequenz > 10:
            print("frequen > 5")
        self.frequenz += 1

    def __eq__(self, other):
        return self.nachname == str(other)


def lemmatize_name(name_string: str) -> Tuple[str, str]:
    for match_pattern in match_patterns:
        if match := match_pattern.fullmatch(name_string):
            nachname = match.group("nachname")
            vornamen = match.group("vornamen")
            return (nachname, vornamen)

    raise ValueError(f"No name format matched to this string: {name_string}")


def get_persons_from_doc(book_name: str, file_name_dat: str, year, names_dict: Dict[str, Nachname]):
    with open(file_name_dat, "rb") as file:
        doc = pickle.load(file)

    for ent in doc.ents:
        if ent.label_ != "PER":
            continue

        ent_text = re.sub("\n", " ", ent.text)
        print("Now:", ent_text)

        try:
            nachname, vornamen = lemmatize_name(ent_text)
        except ValueError as err:
            print(err)
            continue

        if not nachname:
            continue

        # first search for or craete Nachname obj
        if nachname not in names_dict.keys():
            names_dict[nachname] = Nachname(nachname)

        nachname_obj = names_dict[nachname]

        #create Vorkommen
        vorkommen = Vorkommen(book_name, "", year, ent.start, ent.end, ent_text, nachname, vornamen)

        # if we know only the nachname
        if not vornamen:
            nachname_obj.empty_instance.add_vorkommen(vorkommen)
            continue

        # search for matching vornamen
        vornamen_objs = split_up_vornamen(vornamen)
        matched = False
        for name_obj in nachname_obj.name_instanzen:
            if not name_obj.match(vornamen_objs):
                continue
            else:
                name_obj.add_vorkommen(vorkommen)
                name_obj.may_complete_vornamen(vornamen_objs)
                matched = True
                break

        # create new name instance
        if not matched:
            new_name = Name(nachname, vornamen_objs, nachname_obj)
            new_name.add_vorkommen(vorkommen)
            nachname_obj.name_instanzen.append(new_name)

    return names_dict


def get_search_tree():
    # for i in range(1, 51):
    names_dict = {}
    year = 1799
    for i in range(1, 3):
        file_name_dat = f"/mnt/sdb1/cds/data/entities_files/AMZ_wmodel{i}.dat"
        names_dict = get_persons_from_doc(f"AMZ{i}", file_name_dat, year, names_dict)
        year += 1

    return names_dict


def store_vorkommen_in_csv(threshold=10):
    header = ["name", "book", "year", "frequency"]

    csv_file = open("entity_freq_30_1_test.csv", "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    names_dict = get_search_tree()

    for nachname in names_dict.values():
        if nachname.frequenz < threshold:
            continue

        for person in nachname.name_instanzen:
            for year_, vorkommen in person.vorkommen.items():
                csv_writer.writerow([str(person), "AMZ" + str(year_), str(year_), len(vorkommen)])

    csv_file.close()


def store_vorkommen_pickle():
    names_dict = get_search_tree()
    with open("/mnt/sdb1/cds/data/search_tree/search_tree_1_50_pickled.dat", "wb") as file:
        pickle.dump(names_dict, file)

store_vorkommen_pickle()
