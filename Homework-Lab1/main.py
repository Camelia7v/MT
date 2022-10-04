import numpy as np


file = open("lexicon.txt", "r", encoding="utf-8")
lexicon = file.readlines()

for index in range(len(lexicon)):
    lexicon[index] = lexicon[index].split("\n")[0]


file = open("rules.txt", "r", encoding="utf-8")
file_content = file.readlines()

rules = []
for index in range(len(file_content)):
    if "->" in file_content[index]:

        rule = file_content[index].split("\n")[0].split("->")
        first_part = rule[0].split("+")
        second_part = rule[1].split("+")
        final_rule = []

        for rule in first_part:
            final_rule.append(rule.strip())
        for rule in second_part:
            final_rule.append(rule.strip())

        rules.append(final_rule)

print("Rules:                    ", rules, "\n")


translation_dictionary = {}
for line in lexicon:
    if "->" in line:
        words = line.split("->")
        translation_dictionary[words[0].strip().lower()] = words[1].strip().lower()

print("Translation dictionary:   ", translation_dictionary)


pos_dictionary = {}
for i in range(2, len(lexicon)):
    if ":" in lexicon[i] and (lexicon[i+1] != "" or lexicon[i+1] != " "):

        pos_name = lexicon[i].split("(")[0].rstrip()
        pos_dictionary[pos_name] = []

        for j in range(i+1, len(lexicon)):
            if "->" in lexicon[j]:
                pos_dictionary[pos_name] += lexicon[j].split(" -> ")
            else:
                pos_dictionary[pos_name].append(lexicon[j])
            if lexicon[j+1] == "" or lexicon[j+1] == " ":
                break

for key in pos_dictionary:
    for i in range(len(pos_dictionary[key])):
        pos_dictionary[key][i] = pos_dictionary[key][i].rstrip().lower()

print("POS dictionary:           ", pos_dictionary, "\n")


input_strings = ["Mary reads a book", "A book is under the table", "Mary cut the sugar cane with a saw",
                 "Mary cut the sugar cane and is happy",
                 "The woman with a red cane saw a cat under the table and walks to the cat"]

result = []
for i in range(len(input_strings)):
    input_strings[i] = input_strings[i].split(" ")

    translation = ""
    for word in input_strings[i]:
        if word.lower() in translation_dictionary:
            if word[0].isupper():
                translation_word = translation_dictionary[word.lower()]
                translation += translation_word[0].upper() + translation_word[1:] + " "
            else:
                translation += translation_dictionary[word] + " "
        else:
            translation += word + " "
    result.append(translation.rstrip())

print("Translation without rules:", result, "\n")
print(input_strings)


pos_sentences = []
for i in range(len(input_strings)):
    pos_sentence = []
    for word in input_strings[i]:
        for pos in pos_dictionary:
            if word.lower() in pos_dictionary[pos]:
                pos_sentence.append(pos)
                break
    pos_sentences.append(pos_sentence)
print(pos_sentences)


for i in range(len(pos_sentences)):
    for rule in rules:

        # rule: ADJ + N -> N + ADJ
        if rule[0] in pos_sentences[i]:
            index1 = pos_sentences[i].index(rule[0])
            if index1 + 1 < len(pos_sentences[i]) and rule[1] in pos_sentences[i][index1 + 1]:
                pos_sentences[i][index1] = pos_sentences[i][index1 + 1]
                pos_sentences[i][index1 + 1] = rule[3]

                copy = input_strings[i][index1]
                input_strings[i][index1] = input_strings[i][index1 + 1]
                input_strings[i][index1 + 1] = copy

        # rules: The + Masc N -> Le + Masc N
        #        The + Fem N -> La + Fem N
        #        A + Masc N -> Un + Masc N
        #        A + Fem N -> Une + Fem N
        #        saw + DET -> V + DET
        array = np.array(input_strings[i])
        indices1 = list(np.where(array == rule[0])[0])
        for indice in indices1:
            if indice + 1 < len(pos_sentences[i]) and rule[1] in pos_sentences[i][indice + 1]:
                pos_sentences[i][indice] = rule[2]
                pos_sentences[i][indice + 1] = rule[3]

        indices2 = list(np.where(array == rule[0].lower())[0])
        for indice in indices2:
            if indice + 1 < len(pos_sentences[i]) and rule[1] in pos_sentences[i][indice + 1]:
                pos_sentences[i][indice] = rule[2].lower()
                pos_sentences[i][indice + 1] = rule[3]

        # rules: DET + saw -> DET + Fem N
        #        DET + cane -> DET + Fem N
        #        Masc N + cane -> Masc N + ADJ
        #        Fem N + cane -> Fem N + ADJ
        array = np.array(pos_sentences[i])
        indices = list(np.where(array == rule[0])[0])
        for indice in indices:
            if indice + 1 < len(input_strings[i]) and rule[1] in input_strings[i][indice + 1]:
                pos_sentences[i][indice] = rule[2]
                pos_sentences[i][indice + 1] = rule[3]

print(pos_sentences)


final_result = []
for i in range(len(pos_sentences)):
    translated_sentence = ""
    for j in range(len(pos_sentences[i])):
        if pos_sentences[i][j] == "PNOUN":
            translated_sentence += input_strings[i][j] + " "
        elif pos_sentences[i][j] in pos_dictionary:
            index = pos_dictionary[pos_sentences[i][j]].index(input_strings[i][j])
            translated_sentence += pos_dictionary[pos_sentences[i][j]][index + 1] + " "
        else:
            translated_sentence += pos_sentences[i][j] + " "
    final_result.append(translated_sentence.rstrip())

print("\nTranslation with rules:   ", final_result)
