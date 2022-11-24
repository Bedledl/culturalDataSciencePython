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

nlp = spacy.load("de_dep_news_trf")
doc = nlp(long_sentence)
for ent in doc.ents:
    print(ent.text, ent.label_)
