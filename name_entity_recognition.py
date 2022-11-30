from functools import partial

import spacy

long_sentence = "Zum Beweise des oben gesagten folge" \
"hier eine kurze Zergliederung des Werkes "        \
"Es beginnt mit einem Andante, dessen Ge-"        \
"sang nicht einfach genug ist, um sich an-"        \
"genehm singen zu lassen, und nicht künst-"        \
"659 1805.                                   "        \
"lich genug, um durch Neuheit‘ oder Dekla-"        \
""                                                    \
"mation zu überraschen.                      "        \
"Metrum den Komponisten hier und da und      "        \
"dort unsd — sehr oft in Verlegenheit ge-    "        \
"setzt zu haben. Die Verse waren ihm für     "        \
"die gewählte Melodie zu lang; daraus folgt  "        \
""                                           ""       \
"eine widerliche Monotonie: denn beynahe in. "        \
"jedem andern Takt besteht die eine Takt-."        \
"halfte aus zwey, die andere aus vier Syl-"        \
""                                           ""       \
"ben — und so durch das ganze, nicht kur-    "        \
"ge, Gedicht. Die zweyte Strophe ist, Klei-  "        \
"nigkeiten ausgenommen, wie die erste. Bey   "        \
"der dritten Sirophe verlässt Hr. Kanne den  "        \
"Gesang der beyden ersten, und nun folgen    "        \
"einige Strophen hindurch — verba et voces,  "        \
"und Modalationen, die so wenig natürliche,  "        \
"als künstliche Verbindung besitzen, bey de- "        \
"nen man noch überdies die Absicht und den   "        \
"Zweck nicht begreift. Bey den Woorten :     "        \
"Seht, schon naht sie sich ApolVls          "         \
"Altare, steht ein fürchterlicher Uebergang, "        \
"ohne Vorbereitung, und — beynahe möcht      "        \
"ieh sagen, für seine Gesuchtheit, auch ohne "        \
"Motiv, wobey die verba et voces noch im-    "        \
"                                           "         \
"mer ihren irren Gang fortgeheL. — Bis-      "        \
"her war das Monodrama erzählend, nür‘:      "        \
"aber spricht Sappho selbst, und eine Art    "        \
"                                           "         \
"Hymnus beginnt, (in der Poesie nämlich)     "        \
"der sehr schön ist, den aber der Komponist  "        \
"                                           "         \
"ganz ausser Acht gelassen, denn seine voces "        \
"                                           "         \
"gehen immer ihren schleppenden, gleichen    "        \
"Gang, nur mit noch widrigern und sonach     "        \
"zwecklosern Modulationen. Beym höhern       "        \
"Anschwellen von Sappho’s Empfindung, bey    "        \
"ihrem wilder ausbrechenden Schmerz, gehet   "        \
"der Komponist noch immer, unbekümmert       "        \
"um Sappho’s Leiden, seine sandige Strasse   "        \
"fort, ohne Abwechslung des Tempo, der       "        \
"Taktart; nur dass er' von E moll nun nach   "        \
"Es übergeht, wo er aber eben so wenig       "        \
"verweilt, und. wo die schöne Stelle:        "        \
"umsonst bekämpf’ ich diese Schmer-          "        \
"zen etc. eben so matt sich fortträgt, wie   "        \
"alles Uebrige. So bey:                      "        \
"                                           "         \
"Dahey scheint das                           "        \
". nicht erreicht. -                        "         \
"                                           "         \
"Ach i                                       "        \
"                                           "         \
"July. 660                                   "        \
"Phöbus, ach! au deinem süssen Strahle       "        \
"Weidet sich mein Blick zum letzten Malo."

short_sentence = "Er studire nur ferner so fort die Händel, Glck, Bache, und die neu ern Klassiker, Haydn. Morzart, Cherubini und mehrere dergl., wie man sie schon studirt ha ben muss, um etwas wie diese Sonate zu schrei "

test_sen = "Johann Sebastian Bach entstammt der in Mitteldeutschland weitverzweigten lutherischen Familie Bach. Die allermeisten der bis in das 16. Jahrhundert zurückverfolgbaren väterlichen Vorfahren und Verwandte waren Kantoren, Organisten, Stadtpfeifer, Mitglieder von Hofkapellen oder Instrumentenbauer (Clavichord, Cembalo, Laute) zwischen Werra und Saale.[4] Der Stammbaum der Familie Bach lässt sich zurückführen bis zu seinem Ururgroßvater Veit Bach, der als evangelischer Glaubensflüchtling Ungarn oder Mähren[5] verließ und sich in Wechmar bei Gotha, der Heimat seiner Vorfahren, als Bäcker niederließ. Er spielte bereits das Cithrinchen, ein Zupfinstrument. Sein Sohn Johannes Bach war nicht nur als Bäcker, sondern auch als „Spielmann“ tätig. Die weiteren Nachfahren waren alle Musiker. Von Johann Sebastian Bach selbst stammt eine Chronik über den „Ursprung der musicalisch-Bachischen Familie“ mit Kurzbiographien von 53 Familienmitgliedern aus dem Jahr 1735. "

#nlp = spacy.load('de_dep_news_trf')

models = ["de_core_news_sm", "de_core_news_md", "de_core_news_lg"]

mozart_count = {model: [] for model in models}
mozart_count_diffs = {model: [] for model in models}

with open("pre-AMZ3.txt") as file:
    s = file.read()

for model in models:
    nlp = spacy.load(model)

    offset = 0

    while offset < len(s):
        part_text = s[offset:offset + 50000]
        offset = offset + 50000

        doc = nlp(part_text)
        for ent in doc.ents:
            if str(ent.label_) == "PER" and "Bach" in ent.text:
                k = f"{ent.text} {ent.start_char} {ent.end_char}"
                mozart_count[model].append(k)

print(mozart_count)

l1, l2, l3 = mozart_count.values()
values = set(l1 + l2 + l3)
for l in values:
    in_l1 = False
    in_l2 = False
    in_l3 = False

    if l in l1:
        l1.remove(l)
        in_l1 = True

    if l in l2:
        l2.remove(l)
        in_l2 = True

    if l in l3:
        l3.remove(l)
        in_l3 = True

    if in_l1 and in_l2 and in_l3:
        continue

    if in_l1:
        mozart_count_diffs["de_core_news_sm"].append(l)
    if in_l2:
        mozart_count_diffs["de_core_news_md"].append(l)
    if in_l3:
        mozart_count_diffs["de_core_news_lg"].append(l)

print(mozart_count_diffs)

i = 0
def print_colums(i1, i2, i3):
    next_call = None
    if len(i1) > 75 or len(i1) > 75 or len(i1) > 75:
        next_call = partial(print_colums, i1[75:], i2[:75], i3[:75])

    text = i1[:75]
    text += " " * (80 - len(i1[:75]))
    text += i2[:75]
    text += " " * (80 - len(i2[:75]))
    text += i3[:75]
    text += " " * (80 - len(i3[:75]))
    print(text)
    if next_call:
        next_call()


i = 0
while True:
    f = 0
    try:
        i1 = mozart_count_diffs["de_core_news_sm"][i]
    except IndexError:
        f +=1
        pass
    try:
        i2 = mozart_count_diffs["de_core_news_md"][i]
    except IndexError:
        f +=1
        pass
    try:
        i3 = mozart_count_diffs["de_core_news_lg"][i]
    except IndexError:
        f+= 1
        pass
    print_colums(i1, i2, i3)
    i += 1
    if f == 3:
        break