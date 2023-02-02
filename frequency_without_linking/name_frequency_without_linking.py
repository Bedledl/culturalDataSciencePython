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

anreden = ["Mad\.", "Herrn ", "Hr\.", "Hrn\.", "Herr ", "Dem\.", "Madame ", "Madamoiselle ",
           "Demoiselle ", "Frau ", "Herrn ", "Fräulein ", "Miss ", "Mr ", "Mr\."]
funktion = ["Kapellmeister", "Kapellm\.", "Organist", "Kammermusikus", "Conzertmeister", "Concertmeister"
            "Musikdirector", "Musikdireetor", "Kantor", "Cantor", "Musikdirector", "Musikdireotors"]
zwischenwort = ["van", "von", "de"]

REGEX_ZWISCHENWORT = f"({'|'.join(anreden)})"
REGEX_NACHNAME = f"(?P<nachname>({REGEX_ZWISCHENWORT}\s)?[^(\W|\d|_)]*)"
REGEX_ANREDEN = f"(({'|'.join(anreden)})\s?)"
REGEX_FUNKTION = f"(({'|'.join(funktion)})\s?)"
#REGEX_VORNAME_ABKÜRZUNG = "([^(\W|\d|_)]{1,2}\.?)"
REGEX_VORNAME = "([^(\W|\d|_)]*\.?)"
REGEX_VORNAMEN = f"(?P<vornamen>({REGEX_VORNAME}\s){{0,3}}?)"
REGEX_VORNAMEN_NACHGESTELLT = f"(?P<vornamen>({REGEX_VORNAME}?(\s{REGEX_VORNAME}){{0,2}}))"


match_patterns = [
    # "Hr. W. A. Mozart"
    re.compile(f"{REGEX_ANREDEN}?{REGEX_FUNKTION}?{REGEX_VORNAMEN}??{REGEX_NACHNAME}"),
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
    def __init__(self, vorname: str):
        self.abgekürzt = False
        self.vorname = vorname

    def match(self, vorname: 'Vorname'):
        if len(vorname.vorname) > len(self.vorname):
            return vorname.vorname.lower().startswith(self.vorname.lower())
        elif len(self.vorname) > len(vorname.vorname):
            return self.vorname.lower().startswith(vorname.vorname.lower())
        else:
            vn1 = self.vorname.lower()
            vn2 = vorname.vorname.lower()
            vn1 = re.sub("c", "k", vn1)
            vn2 = re.sub("c", "k", vn2)
            return vn1 == vn2

    def complete(self, vorname: 'Vorname'):
        if len(vorname.vorname) > len(self.vorname):
            self.vorname = vorname.vorname

    def __str__(self):
        return self.vorname


def split_up_vornamen(vornamen_str: str) -> List[Vorname]:
    vornamen = []

    vornamen_str_split = vornamen_str.split()
    for vorname in vornamen_str_split:
        vorname = vorname.strip('.')
        if re.fullmatch(REGEX_VORNAME, vorname):
            vornamen.append(Vorname(vorname))
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

    def anzahl_vorkommen(self):
        anzahl = 0
        for vorkommmen_list in self.vorkommen.values():
            anzahl += len(vorkommmen_list)
        return anzahl

    def match(self, vornamen: List[Vorname]) -> bool:
        self_vornamen = self.vornamen
        if len(vornamen) != len(self_vornamen):
            # vielleicht fehlen die ersten Namen
            for vn1, vn2 in zip(reversed(vornamen), reversed(self_vornamen)):
                if vn1.match(vn2):
                    continue
                print("No match 3")
                print([str(v) for v in vornamen], [str(v) for v in self_vornamen])
                break
            else:
                print("match 4")
                print([str(v) for v in vornamen], [str(v) for v in self_vornamen])
                return True

            # vielleicht fehlen die letzten Namen
            # dieser fall sollte durch zip gedeckt sein

        for vn1, vn2 in zip(vornamen, self_vornamen):
            if vn1.match(vn2):
                continue
            print("5")
            print([str(v) for v in vornamen], [str(v) for v in self_vornamen])
            return False

        return True

    def may_complete_vornamen(self, vornamen: List[Vorname]):
        # only execture if vornamen are matching!
        if not self.match(vornamen):
            return

        if len(vornamen) == len(self.vornamen):
            for vn1, vn2 in zip(vornamen, self.vornamen):
                vn2.complete(vn1)

        elif len(vornamen) > len(self.vornamen):
            for vn1, vn2 in zip(reversed(vornamen), reversed(self.vornamen)):
                if vn1.match(vn2):
                    vn2.complete(vn1)
                    continue
                break
            else:
                self.vornamen = vornamen[:len(vornamen) - len(self.vornamen)]
                return

            for vn1, vn2 in zip(vornamen, self.vornamen):
                if vn1.match(vn2):
                    vn2.complete(vn1)
                    continue
                break
            else:
                self.vornamen = self.vornamen + vornamen[len(self.vornamen):]

    def __str__(self):
        return ' '.join([v.vorname for v in self.vornamen] + [self.nachname])

    def add_name_instance(self, other: 'Name'):
        if type(other) != Name:
            raise ValueError(f"Cannot add {type(other)} to Name Obj.")

        if self.nachname != other.nachname:
            raise ValueError(f"Unterscheidliche Nachnamen beim mergen {self.nachname, other.nachname}")

        for _, vorkommen_list in other.vorkommen.items():
            for vorkommen in vorkommen_list:
                self.add_vorkommen(vorkommen)


class Nachname:
    def __init__(self, nachname: str):
        self.nachname = nachname
        self.name_instanzen = []
        self.unentschiedene = []
        self.empty_instance = Name(self.nachname, [], self)

    def frequenz(self) -> int:
        i = 0
        i += self.empty_instance.anzahl_vorkommen()
        for name in self.name_instanzen:
            i += name.anzahl_vorkommen()
        for name in self.unentschiedene:
            i += name.anzahl_vorkommen()
        return i

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

        if nachname[0].islower():
            nachname = nachname[0].upper() + nachname[1:]

        print("Nachname", nachname)
        print("Vorname", vornamen)

        if nachname in  ["Müller", "Bach"]:
            print("asjdfk")

        # first search for or craete Nachname obj
        if nachname not in names_dict.keys():
            if nachname[-1] == "s":
                if nachname[:-1] in names_dict.keys():
                    nachname = nachname[:-1]
                    print(f"correcting nachname: {nachname}")

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
        matches = []
        for name_obj in nachname_obj.name_instanzen:
            if name_obj.match(vornamen_objs):
                matches.append(name_obj)

        if len(matches) == 1:
            matches[0].add_vorkommen(vorkommen)
            matches[0].may_complete_vornamen(vornamen_objs)
        elif len(matches) > 1:
            new_name = Name(nachname, vornamen_objs, nachname_obj)
            new_name.add_vorkommen(vorkommen)
            nachname_obj.unentschiedene.append(new_name)
        else:
            # create new name instance
            new_name = Name(nachname, vornamen_objs, nachname_obj)
            new_name.add_vorkommen(vorkommen)
            nachname_obj.name_instanzen.append(new_name)

    return names_dict


def get_search_tree():
    # for i in range(1, 51):
    names_dict = {}
    year = 1799
#    for i in range(1, 51):
    for i in range(1, 5):
        file_name_dat = f"/mnt/sdb1/cds/data/entities_files/AMZ_wmodel{i}.dat"
        names_dict = get_persons_from_doc(f"AMZ{year}", file_name_dat, year, names_dict)
        year += 1

#    for i in range(63, 83):
    for i in range(63, 67):
        file_name_dat = f"/mnt/sdb1/cds/data/entities_files/AMZ_wmodel{i}.dat"
        names_dict = get_persons_from_doc(f"AMZ{i}", file_name_dat, 1800 + i, names_dict)
        year += 1

    return names_dict


def preprocess_search_tree(names_dict: Dict[str, Nachname], threshold=0):
    return_dict = {}

    for name_str, nachname in names_dict.items():
        if name_str[-1] == 's':
            if name_str[:-1] in names_dict.keys():
                new_nachname = names_dict[name_str[:-1]]

                nachname.empty_instance.nachname = new_nachname.nachname
                new_nachname.empty_instance.add_name_instance(nachname.empty_instance)

                for person in nachname.name_instanzen + nachname.unentschiedene:
                    person.nachname = new_nachname.nachname
                    person.nachname_obj = new_nachname

                    matches = []
                    for person_iter in new_nachname.name_instanzen:
                        if person_iter.match(person.vornamen):
                            matches.append(person_iter)

                    if len(matches) == 0:
                        new_nachname.name_instanzen.append(person)
                    elif len(matches) == 1:
                        matches[0].add_name_instance(person)
                    else:
                        new_nachname.unentschiedene.append(person)

                nachname.name_instanzen = []
                nachname.unentschiedene = []
                nachname.empty_instance.vorkommen = {}

    for name_str, nachname in names_dict.items():
        if nachname.frequenz() < threshold:
            continue

        # add vorkommen empty instance to most frequent vornamen + nachnamen
        if len(nachname.name_instanzen) > 0:
            most_frequent_name = max(nachname.name_instanzen, key=lambda name: name.anzahl_vorkommen())
            most_frequent_name.add_name_instance(nachname.empty_instance)
        else:
            nachname.name_instanzen.append(nachname.empty_instance)

        for unentschieden_name in nachname.unentschiedene:
            matches = []
            for name_iter in nachname.name_instanzen:
                if name_iter.match(unentschieden_name.vornamen):
                    matches.append(name_iter)

            if len(matches) == 0:
                nachname.name_instanzen.append(unentschieden_name)
            elif len(matches) == 1:
                matches[0].add_name_instance(unentschieden_name)
            else:
                match_ = max(matches, key=lambda n: n.anzahl_vorkommen())
                match_.add_name_instance(unentschieden_name)

        return_dict[name_str] = nachname

    return return_dict


def store_vorkommen_in_csv(threshold=0):
    header = ["name", "book", "year", "frequency"]

    csv_file = open("entity_freq_1_2_whole.csv", "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    names_dict = get_search_tree()
    names_dict = preprocess_search_tree(names_dict, threshold)

    for nachname in names_dict.values():
        for person in nachname.name_instanzen:
            for year_, vorkommen in person.vorkommen.items():
                csv_writer.writerow([str(person), "AMZ" + str(year_), str(year_), len(vorkommen)])

    csv_file.close()


def store_vorkommen_pickle(threshold=0):
    names_dict = get_search_tree()
    names_dict = preprocess_search_tree(names_dict, threshold)
    with open("/mnt/sdb1/cds/data/search_tree/search_tree_1_50_pickled.dat", "wb") as file:
        pickle.dump(names_dict, file)

store_vorkommen_in_csv(10)
