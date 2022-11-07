import re


def fill_matrix_with_zeros(row_count, col_count):
    matrix = []
    for i in range(row_count):
        row_list = []
        for j in range(col_count):
            row_list.append(0)
        matrix.append(row_list)

    return matrix


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def extract_numbers_from_string(string):
    return [int(i) for i in string.split() if i.isdigit()]


def extract_source_sentence_and_alignments(source_sentence_with_alignments):
    splited_sentence = re.split(r'(\(\{ (\d? ?)*\}\))', source_sentence_with_alignments)

    sentence = []
    for i in range(3, len(splited_sentence)):
        if splited_sentence[i] != '':
            sentence.append(splited_sentence[i])
    # print(sentence)

    source_sentence = ""
    for i in range(0, len(sentence), 2):
        source_sentence += sentence[i].rstrip()

    alignments = []
    for i in range(1, len(sentence), 2):
        alignments.append(extract_numbers_from_string(sentence[i]))

    return source_sentence.lstrip(), alignments


def create_alignments_table(table, source_sentence, alignment):
    j = 0
    for i in range(len(source_sentence.split(" "))):
        if alignment[i]:
            table[alignment[i][0] - 1][j] = 1
        j += 1
    return table


def return_indices(index1, index2):
    result = ''
    for i in range(index1, index2):
        result += str(i)
    return result


def extract_consistent_phrases(table):
    consistent_phrases = set()
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == 1:
                if 1 not in table[i][j + 1:] and 1 not in table[i][:j]:
                    k = i + 1
                    flag = 0
                    while k < len(table):
                        if table[k][j] == 1:
                            flag = 1
                            break
                        k += 1

                    if i > 0:
                        k1 = i - 1
                        flag1 = 0
                        while k1 >= 0:
                            if table[k1][j] == 1:
                                flag1 = 1
                                break
                            k1 -= 1

                        if flag == 0 and flag1 == 0:
                            consistent_phrases.add((str(i), str(j)))
                    else:
                        if flag == 0:
                            consistent_phrases.add((str(i), str(j)))

            if j > 0:
                copy_of_i = i
                while copy_of_i < len(table):
                    if 1 in table[copy_of_i][copy_of_i:j + 1] and 1 not in table[copy_of_i][:copy_of_i] and 1 not in \
                            table[copy_of_i][j + 1:]:
                        k = copy_of_i + 1
                        while k < len(table):
                            if 1 in table[k][k:j + 1]:
                                l = k + 1
                                flag2 = 0
                                while l < len(table):
                                    if 1 in table[l][l:j + 1]:
                                        flag2 = 1
                                        break
                                    l += 1
                                if flag2 == 0:
                                    consistent_phrases.add(
                                        (return_indices(copy_of_i, j + 1), return_indices(copy_of_i, j + 1)))
                            k += 1
                    copy_of_i += 1

            if table[i][j] == 1:
                if 1 not in table[i][:j] and 1 not in table[i][j + 1:]:
                    if i > 0:
                        k = i - 1
                        flag = 0
                        while k >= 0:
                            if table[k][j] == 1:
                                flag = 1
                                break
                            k -= 1
                        if flag == 0:
                            l = i + 1
                            l1 = i
                            while l < len(table):
                                if table[l][j] == 0:
                                    break
                                l += 1
                            consistent_phrases.add((return_indices(l1, l), str(j)))

            if table[i][j] == 1:
                if 1 not in table[i][:j] and 1 not in table[i][j + 1:]:
                    if i > 0:
                        k = i - 1
                        while k >= 0:
                            if 1 in table[k]:
                                break
                            else:
                                consistent_phrases.add((return_indices(k, j + 1), return_indices(k, j + 1)))
                                consistent_phrases.add((return_indices(k, j + 1), return_indices(j, j + 2)))
                            k -= 1
                    l = i + 1
                    while l < len(table):
                        if 1 in table[l]:
                            break
                        else:
                            consistent_phrases.add((return_indices(l, j + 1), return_indices(l, j + 1)))
                            consistent_phrases.add((return_indices(l - 1, l + 1), return_indices(j, j + 2)))
                        l += 1

    consistent_phrases_list = []
    consistent_phrases = list(consistent_phrases)
    for i in range(len(consistent_phrases)):
        if '' not in consistent_phrases[i]:
            consistent_phrases_list.append(consistent_phrases[i])

    return consistent_phrases_list


def symmetrizationroen(source, target, allignment):
    listenro = []
    i = 0
    for alignment_one in allignment:
        if len(alignment_one) == 1:
            listenro.append((source[i], target[alignment_one[0] - 1]))
        i += 1
    return listenro

def symmetrizationenro(source, target, allignment):
    listenro = []
    i = 0
    for alignment_one in allignment:
        if len(alignment_one) == 1:
            listenro.append((target[alignment_one[0] - 1], source[i]))
        i += 1
    return listenro

if __name__ == "__main__":

    print("------------------------------------> RO-EN:")
    with open("alignments1.txt", 'r') as alignments_file1:
        lines1 = alignments_file1.readlines()

    target_sentences1 = []
    source_sentences_with_alignments1 = []
    for i in range(0, len(lines1), 3):
        target_sentences1.append(lines1[i + 1].split("\n")[0])
        source_sentences_with_alignments1.append(lines1[i + 2].split("\n")[0])

    print("Target sentences:", target_sentences1)
    print("Source sentences with alignments:", source_sentences_with_alignments1)

    source_sentences1 = []
    alignments1 = []
    for i in range(len(source_sentences_with_alignments1)):
        source_sentence, alignment = extract_source_sentence_and_alignments(source_sentences_with_alignments1[i])
        source_sentences1.append(source_sentence)
        alignments1.append(alignment)

    print("Source sentences:", source_sentences1)
    print("Alignments:", alignments1)
    print()

    for i in range(len(source_sentences1)):
        print(f"------------------------------------ Table {i + 1} ------------------------------------")
        table = fill_matrix_with_zeros(len(target_sentences1[i].split(" ")), len(source_sentences1[i].split(" ")))
        print_matrix(create_alignments_table(table, source_sentences1[i], alignments1[i]))
        print()
        print(extract_consistent_phrases(table))
        print()

    print("------------------------------------> EN-RO:")
    with open("alignments2.txt", 'r') as alignments_file2:
        lines2 = alignments_file2.readlines()

    target_sentences2 = []
    source_sentences_with_alignments2 = []
    for i in range(0, len(lines2), 3):
        target_sentences2.append(lines2[i + 1].split("\n")[0])
        source_sentences_with_alignments2.append(lines2[i + 2].split("\n")[0])

    print("Target sentences:", target_sentences2)
    print("Source sentences with alignments:", source_sentences_with_alignments2)

    source_sentences2 = []
    alignments2 = []
    for i in range(len(source_sentences_with_alignments2)):
        source_sentence, alignment = extract_source_sentence_and_alignments(source_sentences_with_alignments2[i])
        source_sentences2.append(source_sentence)
        alignments2.append(alignment)

    print("Source sentences:", source_sentences2)
    print("Alignments:", alignments2)
    print()

    for i in range(len(source_sentences2)):
        print(f"------------------------------------ Table {i + 4} ------------------------------------")
        table = fill_matrix_with_zeros(len(target_sentences2[i].split(" ")), len(source_sentences2[i].split(" ")))
        print_matrix(create_alignments_table(table, source_sentences2[i], alignments2[i]))
        print()
        print(extract_consistent_phrases(table))
        print()

    setenro = []
    setroen = []

    s = 'I want to go home'
    t = 'Je veux aller chez moi'
    a1 = [[1],[2],[3],[3],[5]]
    a2 = [[1],[2],[4],[5],[5]]
    setroen.append(symmetrizationenro(s.split(" "),t.split(" "),a1))
    setenro.append(symmetrizationroen(t.split(" "), s.split(" "), a2))
    allenro = setroen[0] + setenro[0]
    allenro = list(dict.fromkeys(allenro))
    print(allenro)

    setenro = []
    setroen = []

    for source, target, allignment in zip(source_sentences1, target_sentences1, alignments1):
        setenro.append(symmetrizationenro(source.split(" "), target.split(" "), allignment))
    for source, target, allignment in zip(source_sentences2, target_sentences2, alignments2):
        setroen.append(symmetrizationroen(source.split(" "), target.split(" "), allignment))
    for i in range(len(setroen)):
        allenro = setroen[i] + setenro[i]
        allenro = list(dict.fromkeys(allenro))
        print(allenro)

    # table = [[1, 0, 0],
    #          [0, 1, 0],
    #          [0, 0, 1]]

    # table = [[0, 0, 0],
    #          [0, 1, 0],
    #          [0, 0, 0]]

    # table = [[1, 0, 1],
    #          [0, 1, 0],
    #          [0, 1, 0]]
