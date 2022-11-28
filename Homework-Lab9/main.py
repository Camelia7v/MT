"""
TASK:
 Transform the lexical n-gram language model for Romanian that you have already implemented into a POS n-gram model.
"""

from bs4 import BeautifulSoup
import requests
# nltk.download('punkt')

import spacy
nlp = spacy.load("ro_core_news_sm")
# python -m spacy download ro_core_news_sm

import nltk.data


def create_corpus(page_link):
    # get URL
    page = requests.get(page_link)

    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)

    # write text into a file
    f = open("corpus.txt", "wb")
    for item in soup.find_all('p'):
        f.write(item.get_text().encode("UTF-8"))
    f.close()


def get_POS_for_words():
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    text = open("corpus.txt", "r", encoding="utf-8").read()
    list_of_sentences = tokenizer.tokenize(text)

    POSs = []
    sentence_POSs = []
    unique_POSs = set()
    POSs_counter = 0
    for sentence in list_of_sentences:
        sentence = nlp(sentence)
        print(sentence)
        for token in sentence:
            if token.pos_ != '':
                sentence_POSs.append(token.pos_)
                unique_POSs.add(token.pos_)
                POSs_counter += 1
                print(token, token.pos_)
        POSs.append(sentence_POSs)
        print("-------------------------------------------------------------"
              "-------------------------------------------------------------")

    print("All the POSs from the corpus: ", POSs_counter)
    print("All the UNIQUE POSs from the corpus: ", len(unique_POSs))

    return POSs, unique_POSs


def get_language_model(POSs_list, unique_POSs, n):
    V = len(unique_POSs)

    if n == 2:
        list_of_bigrams = []
        bigram_counts = {}
        unigram_counts = {}

        for POSs in POSs_list:
            for i in range(len(POSs) - 1):
                if i < len(POSs) - 1:
                    list_of_bigrams.append((POSs[i], POSs[i + 1]))

                    if (POSs[i], POSs[i + 1]) in bigram_counts:
                        bigram_counts[(POSs[i], POSs[i + 1])] += 1
                    else:
                        bigram_counts[(POSs[i], POSs[i + 1])] = 1

                if POSs[i] in unigram_counts:
                    unigram_counts[POSs[i]] += 1
                else:
                    unigram_counts[POSs[i]] = 1

        print("\n All the possible Bigrams are: ")
        print(list_of_bigrams)

        print("\n Bigrams along with their frequency: ")
        print(bigram_counts)

        print("\n Unigrams along with their frequency: ")
        print(unigram_counts)

        list_of_probabilities = {}
        for bigram in list_of_bigrams:
            word1 = bigram[0]
            list_of_probabilities[bigram] = (bigram_counts.get(bigram) + 1) / (unigram_counts.get(word1) + V)

        print("\n Bigrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_bigrams, bigram_counts, unigram_counts

    elif n == 3:
        list_of_trigrams = []
        trigram_counts = {}
        bigram_counts = {}

        for POSs in POSs_list:
            for i in range(len(POSs) - 1):
                if i < len(POSs) - 2:
                    list_of_trigrams.append((POSs[i], POSs[i + 1], POSs[i + 2]))

                    if (POSs[i], POSs[i + 1], POSs[i + 2]) in trigram_counts:
                        trigram_counts[(POSs[i], POSs[i + 1], POSs[i + 2])] += 1
                    else:
                        trigram_counts[(POSs[i], POSs[i + 1], POSs[i + 2])] = 1

                if (POSs[i], POSs[i + 1]) in bigram_counts:
                    bigram_counts[(POSs[i], POSs[i + 1])] += 1
                else:
                    bigram_counts[(POSs[i], POSs[i + 1])] = 1

        print("\n All the possible Trigrams are: ")
        print(list_of_trigrams)

        print("\n Trigrams along with their frequency: ")
        print(trigram_counts)

        print("\n Bigrams along with their frequency: ")
        print(bigram_counts)

        list_of_probabilities = {}
        for trigram in list_of_trigrams:
            word1 = trigram[0]
            word2 = trigram[1]
            list_of_probabilities[trigram] = (trigram_counts.get(trigram) + 1) / (bigram_counts.get((word1, word2)) + V)

        print("\n Trigrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_trigrams, trigram_counts, bigram_counts

    elif n == 4:
        list_of_tetragrams = []
        tetragrams_counts = {}
        trigram_counts = {}

        for POSs in POSs_list:
            for i in range(len(POSs) - 1):
                if i < len(POSs) - 3:
                    list_of_tetragrams.append((POSs[i], POSs[i + 1], POSs[i + 2], POSs[i + 3]))

                    if (POSs[i], POSs[i + 1], POSs[i + 2], POSs[i + 3]) in tetragrams_counts:
                        tetragrams_counts[(POSs[i], POSs[i + 1], POSs[i + 2], POSs[i + 3])] += 1
                    else:
                        tetragrams_counts[(POSs[i], POSs[i + 1], POSs[i + 2], POSs[i + 3])] = 1

                    if (POSs[i], POSs[i + 1], POSs[i + 2]) in trigram_counts:
                        trigram_counts[(POSs[i], POSs[i + 1], POSs[i + 2])] += 1
                    else:
                        trigram_counts[(POSs[i], POSs[i + 1], POSs[i + 2])] = 1

        print("\n All the possible Tetragrams are: ")
        print(list_of_tetragrams)

        print("\n Tetragrams along with their frequency: ")
        print(tetragrams_counts)

        print("\n Trigrams along with their frequency: ")
        print(trigram_counts)

        list_of_probabilities = {}
        for tetragram in list_of_tetragrams:
            word1 = tetragram[0]
            word2 = tetragram[1]
            word3 = tetragram[2]
            list_of_probabilities[tetragram] = \
                (tetragrams_counts.get(tetragram) + 1) / (trigram_counts.get((word1, word2, word3)) + V)

        print("\n Tetragrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_tetragrams, tetragrams_counts, trigram_counts


def get_probability_for_a_new_text(n, input_text_POS, unique_POSs, POSs, list_of_probabilities,
                                   list_of_tuples, tuples_counts, tuples_minus_1_counts):
    V = len(unique_POSs)
    input_words = input_text_POS.rstrip().split(" ")
    tuples = []

    if n == 2:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 1:
                tuples.append((input_words[i], input_words[i + 1]))
        print("\n The bigrams in given sentence are: ")
        print(tuples)
    elif n == 3:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 2:
                tuples.append((input_words[i], input_words[i + 1], input_words[i + 2]))
        print("\n The trigrams in given sentence are: ")
        print(tuples)
    elif n == 4:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 3:
                tuples.append((input_words[i], input_words[i + 1], input_words[i + 2], input_words[i + 3]))
        print("\n The tetragrams in given sentence are: ")
        print(tuples)

    count = 0
    for item in input_words:
        if item not in POSs:
            count += 1

    print("\n The probabilities for the tuples are: ")
    sentence_probability = 1
    if count == 0:
        for i in range(len(tuples)):
            print('0: ', list_of_probabilities[tuples[i]])
            sentence_probability *= list_of_probabilities[tuples[i]]
    else:
        for i in range(len(tuples)):
            if tuples[i] in list_of_tuples:
                if len(tuples[i]) == 2:
                    probability = (tuples_counts[tuples[i]] + 1) / (
                            tuples_minus_1_counts[tuples[i][0]] + V)
                    print('1: ', probability)
                    sentence_probability *= probability
                else:
                    probability = (tuples_counts[tuples[i]] + 1) / (
                                tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V)
                    print('1: ', probability)
                    sentence_probability *= probability
            elif tuples[i][:len(tuples[i]) - 1] in tuples_minus_1_counts:
                print('2: ', 1 / (tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V))
                sentence_probability *= 1 / (tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V)
            else:
                print('3: ', 1 / V)
                sentence_probability *= 1 / V

    print('\n' + f'The probability of sentence "{input_text_POS.rstrip()}" is ' + str(sentence_probability))


if __name__ == "__main__":
    webpage_link = "https://ro.wikipedia.org/wiki/Cel_mai_iubit_dintre_pământeni_(roman)"

    input_text = "Cel mai iubit dintre pământeni"
    # input_text = "Titlul romanului poate fi citit ca semn al pledoariei disperate pe care autorul o face"

    # input_text = input("Enter a sentence (in Romanian): ")
    n = int(input("Enter a value for n (it can be 2, 3 or 4): "))

    input_text = nlp(input_text)
    input_text_POS = ''
    for token in input_text:
        input_text_POS += token.pos_ + ' '

    POSs, unique_POSs = get_POS_for_words()
    list_of_probabilities, list_of_tuples, tuples_counts, tuples_minus_1_counts = \
        get_language_model(POSs, unique_POSs, n)
    get_probability_for_a_new_text(n, input_text_POS, unique_POSs, POSs, list_of_probabilities,
                                   list_of_tuples, tuples_counts, tuples_minus_1_counts)
