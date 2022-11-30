import spacy
from spacy.language import Language
from spacy_hunspell import spaCyHunSpell
from spacy.training import Example
from spacy.tokens import Doc

from Composer import Composer
from createWordList import get_pickled_composers, get_buckets_from_file

entities_raw = []
entities_hunspell = []
entities_trained = []

nlp = spacy.load('de_core_news_lg')
# with open("pre-AMZ3.txt") as file:
#    s = file.read()

s = "Mozarts, Sammtliche Werke:  -- - Klaviersachen, gr Hefr. Pranumerationspreis  Her Kapellmeister Reichardt wird, seiner; Aeufserung gegen uns nach, vornehmlich weil er in der vor ver schiednen Jahren herausgekommenen Berliner musikali eschen Zeitung die musikalisch - kritischen Aruukel allein  beiter an den in unsern Blattern erscheinenden Recensio.  schreibt - . >>einige junge Komponisten, die inmer nicht begreifen mogen, wie sie anders, als aus hamischen Ne benabsichten, die sie rechtlichen Leuten so gerne andich ten, getadelt werden konnten, uber seinen vermeynten grofsen Antheil an dem kritischen Theil der musik. Zeit. ungebuhrlich laut geworden sind: so findet er sich ver. | anlafst, uns aufzuforderu, wir mochten uns uber sein Theilnehmen an jenen Artikeln unsrer Blatter, und aber ein ihm zugeschriebnes Verhalitnis zur Redaktion dersel ben erklaten. Wir erklaren demnach ganz bestimmt: der Herr Kapellmeister Reichardt hat an der Redak tion dieser Zeitung von ihrein Entstehen an nicht den ge ringsten Antheil gehabt, und hat ihn auch jezt nicht; von den Recensionen aller drey Jahrgange ist nur eine einzige, ond zwar eines theatralischen Werks, von ihm. Leipzig, Anfang des Jali 1801. Die Redaktion der musik. Zeitung. Die Verlagshandlung der musik. Zeitung.  . -- N 1Thlr. 12 cr. Ladenpreis 3 Thlr. , Ankund igun 8- -- Partitaren. No. 2. Don Jvan oder der steinerne Gast. Eine komische Operin 2 Aufzugen, mit unter- . ------------rs6  legtem deutszhen Texte nebst isimmtlichen vom Konm povnisten spater eingelegten Stucken. In Partitur, Ladenpreis i12 Thlr. | -- ----- Klavier. Concerte. No. 6. Ladenpreis a Thle. -- -- OQoartetten. m. emhalt 3 Quart. Pranumerations preis i Thlr.. Ladenpreis 2 Thlr. | --.--. ->2n...,5- Ladenpreis 2 Thir. -- --- Conecert pour Clarinette avec ace de 2 Violons, 2 Flutes, 2 Bassons, 2 Cors, Viola et Passe 2 Thlr. -----Lle meme Conrert arrange pfour la Flite traver siere avec accomp. de a Violons, a Hautbois, 2 Cors,  Unterzeichneter giebt sich die Ehre, dem musikali schen Poblikum hiermit bekannt zu machen, dafs es ihm nach unendlichen Versuclhen und betrachlichem Kostenauf. wandgelungenist, die sogenannten Cinellen, oder turkischen Becken, welche bey der Janitscharen - Musik gebraucht werden, und die men bisher nur in der Turkey machie, selbst zu verfertigen.  Da sein Fabrikat den Beyfell aller Kenner erhalten hat. so ist er von der hohen niederosterreichischen Landesregierung mit einem Privilegium privativum dar uber begnadigt worden. j 43  2 Bassons, Viola et Basse, par A. E. Muller. z Thlr.  Mezart, Pieces d'harmonie p. 2 Clarinettes, 2 Hautbois, z Bassons et z Cors, Liv. i. No.. 2.3. 3 Thlr.  -- - 4oe.. do. Liy.2. No. 4 et 58. g Thlr.  Romberg, Bernhard,  Viola et Violoncelle. Op. r. Liv. . i Thlr.  Schlimbach, uber die Struktur. Erhaltung, Stimmung  und Prufung der Orgel Mit 5 Kupfertafeln und z Blatt Noten. gr. 8. i Thlr. 8 Gr.  Vogler, Abt. Herrmann von Unna. Ein Schauspiel mit Choren und Tanzen im Klavicrauszug. i Thlr. 12 Gr.  Wolfl, J., Trois Quatuors p. Violon, Violonecelle, Alto et Basse. Op. 1o. Liv.z. 2 Thlr. zt Gr.  -- - 3 Sonates pour le Pianoforte avec accomp. d'un Violon, composzses sur des idees prises de l' Oratoire de Haydn: la Creation. Op. 14. a Thlr.  Zumsteeg, Elwine, eine Ballade vom Freyh. v. Ul menstein. z0vGr.  12 Gr.  -- -- DPDrirey Gesange mit Klavierbegleitung  Neue Muuusikalien, von verschiedenen Verlegern, welche bey Breitkopf und Hartel zu haben sind.  Wanhall, J., 8 deutsche Kinderlieder, am Klavier zu singen. 10 Gr.  Reymann, B. Ch., Concert pour la Harpe accomp. de  2 Violons, Viola, Basse, z Cors et z Obois. Op. 8. 1i Thlr. 16 Gr. ----qag. poor d.0p9 i Thlr. 16 Gr.  Hansel, P.,3 Quartetti per 2 Violini, Viola e Violon cello. Op.8. 2 Thlr. Haydn, J., 3 Quatuors p. 2 Violons, Alio et Violon celle. Op. 32. No.2. Edirion revue et corrigee. z2 Thlr. Haydn, J., 3 Quatuors posur z2 Violons, Taille et Vio loncelle. Op. 45 et 16. a a Thlr. 8Gr. Girowetz, A., Notturno pour le Pianoforte avec acc. d'un Violon et Violoncelle. No, 5 et 6. Op. 34 ei 35. a i Thlr. 8 Gr. , Mozart, W. A., Grand Concert pour le Pianoforte ayv. acc. Op- 687. z Thlr. -- --- Rondo pour le Violon principale avec accomp. Op. 86. i Thlr. Winter, Ouyerture aus dem unterbrochenen Opferfest furs Fortep. mit Begl. einer Violine und Violoncello. - 10 Gr,  3 Quatuors pour z2 Violons  .41  Voigt, LN., Ariette: Lafst die Politiker u. s. w. avec 13 Variations pour le Clav. ou Fortepiano. 10 Gr.  Bliesener, I., Concerto pour Viola principale accomp. de divers Instrumens. Op.8. z2 Thlr. i Gr.  Reichardt, JF., Gesange aus der Oper Tamerlan. No. 1-6. 16 Gr.  -- - Wirsche und Taanze fur's Klavier aus der Oper Tamerlan. 12 Gr.  Beckzwarzowsky, Gesange beyin Klavier. 197 Gr. Hasse, A.G., Serenade pour la Harpe avec accomp. de 2 Flates, 2 Cors de chasse et Basse. Op.6. i16 Gr. Kleinheinz, Sonate pour le Pianoforte. Op. 5. 16 GL  Kreith, Ch., 3 Duos p. 2 Flates. Op.1o. i Thlr..  Kauer, Ferd., Auszug der beliebtesten Stucke aus Mo zarts Zauberflote, frey ubersezt fur das Fortepiano, eine Violin und Violoncelle. 3 Thlr. 8 Gr.  Kreith, C., 3 Duos pour 2 Clarinettes. i Thir. 2 Gr. Wanharll, J., 3Gratulations-Sonaten u. s. w., fur das Pianoforte mit Begleitung einer Violine. i Thlr. 4 Gr. Edel, G., Serfnade pour Violon, Violoncelle et Gui  tarre. Op.7. i18 Gr.  wefifl. J., Sonate p. l Pianoforte av. acc. d'une Flate obligee. Op-3. 16 Gr.  Forster, E. A., Trio p. le Fortepiang, Violon et Vie loncelle. Op. 18. i Thlr. 4Gr.  Heiimerlein, C. J., Concerto pour le Violoncelle av. acc. Op. i. i Thlr. 16 Gr.  Haydn. J., 8 Pieces favorites pour le Clav. ou Pianof av. acce. d'un Violon et Violoncelle ad libitum, tirees des nouvelles Symptonies. Op. 84 i Thir. 19 Gr.  Hansel, P., 3 Themes vauries pour le Violon avec ace. de Viola, Op. 4. 16 Gr.  Conti, J., 3 Duos concertants pour 2 Violons. Op. 10. 1 Thlr. 8 Gr.  Tuch, H.G., Gesange aus Lafontaines Werken mit Klavierbegleitung. is Heft. 128 Werk. i2 Gr."

doc = nlp(s)
for ent in doc.ents:
    if str(ent.label_) == "PER":
        entities_raw.append(f"{ent.text}")


@Language.factory("hunspell")
def create_my_hunspell(nlp, name):
     return spaCyHunSpell(nlp, ("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff"))


#hunspell = create_my_hunspell(nlp, "hunspell")

nlp.add_pipe("hunspell")

composers = get_pickled_composers("composers_spotify.dat")

#get_buckets_from_file("pre-AMZ3.txt", "bucket_file.csv", composers)


composer_names = [composer.last_name for composer in composers] + [composer.name for composer in composers]
#composer_names = ['Abbatini', 'Abeille', 'Abel', 'Abel', 'Abell', 'Abert', 'Abos', 'Abt', 'Accolay', 'Adaiewsky', 'Adam','Addison', 'Adler']

text = "EHanne. Willkommen jetzt, o dunkler Hain,"\
"Wo der bejahrten Eiche Dach"\
". Den kuhlenden Schirm gewahrr,"\
">> Und wo der schlanken Aespe Laub"\
",, . Mit leisem Gelispel rausche!"\
",,- Sie strahl ie scheint.. | Am weichen Moose rieselt da:"\
"a (e strahlt, ,,e sc cn \ In hetler Fluth der Bach,"\
"Chor. Und frohlich summend irrt und wirr. J. S. Bach, aufgebracht daruber, nahm seinen Abschied und ging nach Hamburg."


text2 = "Berbiguier, T., Gollection d’airs connus, arr. en Duos "\
"p- 2 Flütes, ı Suppl a la methode de Flüäte du meme            "\
"auteur, 172.                                                   "\
"                                                               "\
"Bochsa, Notturno p. la Harpe ä crochets et Violon obl. arr.    "\
"p- H. Backofen, 351. -                                         "\
"                                                               "\
"Cramer, J. B., 5me Divert. p. le Pianof. av. ace. . d’une Fl.. "\
"                                                               "\
"ad lib. 680.                                                   "\
"                                                               "\
"Fesca, F. E., Quatuor p. 2 VV. Viola et Vlle. Oeu. 12. 569.    "\
"                                                               "\
"Gabrietsky, G., grand Trio concert. p. 3 Flütes. Oeur. 53      "\
"et 34. 99- |                                                   "\
"                                                               "\
"Gabrielsky, W., 3 Duos concert. p- 2 Flütes, Oeu. 59. 280.     "\
"                                                               "\
"Giorgetti, F.,gr. T rio pour Violoneelle, Violon et Viola,     "\
"Oeuvr. 11. 141.                                                "\
"                                                               "\
"Grund, F. W., Son. p. le Pianof. et Veelle ou Violon, 137.     "\
"                                                               "\
"Hummel, J.N., gr. Trio pour il Pianof. Violine et Veelld       "\
"op- 83. 661.                                                   "\
"                                                               "\
"Kreutzer, Conr., 6 Pieces fac. pour le Pianof. av. accomp.     "\
"d’une Fläte oa Viol. ad lib. Oeuvr. 3..L1. 294.                "\
"                                                               "\
"Lindemann, J. D., 12 Walses, 6 Ecoss. et 2 Sauteuses p.        "\
"2 VV. Fläte, Clharinette, 2 Cors et Basse liv. rı. 204.        "\
"                                                               "\
"de St. Lubin, Leon, gr. Duo p. 2 VV. Oeuvr. 3. 203.            "\
"                                                               "\
"Morgenroth, F., Variat. p. le Violon av. ace. d’un second      "\
"                                                               "\
"Violon, Viola et Basse, Oouvr. a. 584. .                       "\
"Müller, J.J., gr- Quintuor p. le Pianof. av. ace. de a.VV.     "\
"A.et Vlle. op. 17. 677-                                        "\
"Onslow, Ge., 4s, Ss, 6s Trio für Pianef. Violin und Veall.     "\
"148 Werk. n. 1. 2-3. 631."

#doc = nlp("Dittersdorf hatte diese Selbstbiographie abgefasst in den lezten Monaten seines Lebens, wo er an Geist nicht geschwacht, nur gebeugt, aber an Korper gelahmt, ohne alle Fabigkeit sich zu regen, da lag, voiler Sorgen fur die Seinigen, besonders wenn ihn der Tod nicht bald abrufen wurde, dem er aber schneil genug, dire<<y Tage nach Vollendung dieser seiner Biographie, zur Beute wurde.")
#doc = nlp("des Kliavierspielens anschautich mache, zu befriedigem besorgen wit auf künftige Ystermesse eine deutsche Bearbeitung des beliebten Französischen Werks dieser Art von Pleyel und Dussek, Mannern, die gewiss in unsrer Zeit die Achtung des musikalischen Publikums verdient haben. ")
doc = nlp(text2)
for ent in doc.ents:
    if str(ent.label_) == "PER":
        entities_hunspell.append(f"{ent.text}")

for word in doc:
    print(f"{word}: {word._.hunspell_suggest}")



ex_text = " ".join(composer_names)

entities = []
offset = 0
for ent in composer_names:
    entities.append((offset, offset + len(ent), "PER"))
    offset += len(ent) + 1

doc = Doc(nlp.vocab, words=composer_names)
example = Example.from_dict(doc, {"entities": entities})
print("update")
nlp.update([example])


doc = nlp(s)
for ent in doc.ents:
    if str(ent.label_) == "PER":
        entities_trained.append(f"{ent.text}")


print(entities_raw)
print(entities_hunspell)
print(entities_trained)
print(len(entities_raw))
print(len(entities_hunspell))
print(len(entities_trained))
