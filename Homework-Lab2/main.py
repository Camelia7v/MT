from deep_translator import GoogleTranslator


def translate_text(text, source_language, target_language):
    return GoogleTranslator(source=source_language, target=target_language).translate(text)


if __name__ == "__main__":

    text_to_translate = """ 
Stupul lor de pe vâlcea
Stă păzit într-o broboadă
De trei plopi înnalţi, de nea,
Pe o blană de zăpadă.

Prisacarul le-a uitat,
Şi-a căzut si peste ele
Iarna, grea ca un plocat,
Cu chenar de peruzele.

Înlauntru însă-n stup
Lucrătoarele sunt treze Şi făcând un singur trup
Nu-ncetează să lucreze.

Că niciuna n-a muncit
Pentru sine, ci-mpreună
Pentru stupul împlinit
Cu felii de miere bună.
"""

    text_to_translate = """
Amazon.com riscă amenzi de până la 12 milioane de ruble (204.000 de dolari) în Rusia, pentru că nu şterge
conţinutul pe care Moscova îl consideră ilegal, au relatat marţi agenţiile de presă, în ceea ce ar fi prima
penalizare de acest fel pentru gigantul tehnologic din SUA, transmite Reuters.

Rusia a amendat alte câteva firme de tehnologie străine pentru aceeaşi infracţiune, o parte din ceea ce
criticii spun că este o campanie mai amplă a Kremlinului pentru a limita influenţa şi acoperirea companiilor
de tehnologie occidentale în Rusia, informează News.ro.

TASS a citat o instanţă din Moscova care a afirmat că împotriva Amazon au fost întocmite două dosare, ambele
referitoare la ”o încălcare a procedurii de restricţionare a accesului la informaţii”, în conformitate
cu legislaţia rusă.

”(Amazon) se confruntă cu o pedeapsă sub forma unei amenzi în valoare totală de până la 12 milioane de ruble”,
a declarat TASS, care a citat instanţa.

Amazon nu a răspuns imediat unei solicitări de comentarii trimise prin e-mail.

TASS nu a specificat conţinutul care ar fi încălcat legislaţia rusă.

Marţi mai devreme, Tribunalul districtual Tagansky din Moscova a amendat serviciul de streaming al Amazon
Twitch cu 4 milioane de ruble pentru că a găzduit un interviu video cu o personalitate politică ucraineană
despre care Moscova a spus că ar conţine informaţii ”false”.
    """

    # text_to_translate = "Buna ziua!"

    source_language = 'ro'
    target_languages = ['en', 'de', 'fr', 'it', 'ja', 'pt', 'ru', 'sv', 'tr', 'uk', 'ro']

    for target_language in target_languages:
        translation = translate_text(text_to_translate, source_language, target_language)
        print(f"\n---------------------------Translation from {source_language} to"
              f" {target_language}---------------------------")
        print(translation, "\n")
        source_language = target_language
        text_to_translate = translation
