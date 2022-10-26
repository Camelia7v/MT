import math


def compute_probability(english_sentence, foreign_sentence, P):
    probability = 1

    for foreign_word in foreign_sentence:
        probability_sum = 0
        for english_word in english_sentence:
            probability_sum += P[(foreign_word, english_word)]
        probability *= probability_sum

    probability = probability / (len(foreign_sentence) ** len(english_sentence))

    return probability


def compute_perplexity(sentence_pairs, P):
    perplexity = 0

    for pair in sentence_pairs:
        probability = compute_probability(pair[0], pair[1], P)
        perplexity += math.log(probability, 2)

    perplexity = 2.0 ** (-perplexity)
    return perplexity


def initiate_probabilities(P, initial_probability, english_words, foreign_words):
    for english_word in english_words:
        for foreign_word in foreign_words:
            pair = (foreign_word, english_word)
            P[pair] = initial_probability


sentence_pairs = [
    [['NULL', 'the', 'dog'], ['le', 'chien']],
    [['NULL', 'the', 'cat'], ['le', 'chat']]
]
print('No. of sentences in translation memory: ', len(sentence_pairs))
print('Sentences: ', sentence_pairs)


foreign_words = []
english_words = []
for pair in sentence_pairs:
    for english_word in pair[0]:
        english_words.append(english_word)
    for foreign_word in pair[1]:
        foreign_words.append(foreign_word)

english_words = sorted(list(set(english_words)), key=lambda s: s.lower())
foreign_words = sorted(list(set(foreign_words)), key=lambda s: s.lower())
print('English vocabulary: ', english_words)
print('Foreign vocabulary: ', foreign_words)

english_vocab_size = len(english_words)
foreign_vocab_size = len(foreign_words)
print('English vocabulary size: ', english_vocab_size)
print('Foreign vocabulary size: ', foreign_vocab_size, "\n")


print_probabilities = True
no_iterations = 5

perplexities = []
sentence_total = {}
P = {}

initial_probability = 1.0 / foreign_vocab_size
initiate_probabilities(P, initial_probability, english_words, foreign_words)


# Loop while not converged
for iteration in range(no_iterations):

    # Calculate perplexity
    perplexity = compute_perplexity(sentence_pairs, P)
    perplexities.append(perplexity)

    print(f'\n ************** Iteration {iteration + 1} ************** \n')

    total = {}
    tc = {}

    for english_word in english_words:
        total[english_word] = 0.0
        for foreign_word in foreign_words:
            tc[(foreign_word, english_word)] = 0.0

    for pair in sentence_pairs:

        # Compute normalization
        for foreign_word in pair[1]:
            sentence_total[foreign_word] = 0.0
            for english_word in pair[0]:
                sentence_total[foreign_word] += P[(foreign_word, english_word)]

        # Collect counts
        for foreign_word in pair[1]:
            for english_word in pair[0]:
                tc[(foreign_word, english_word)] += P[(foreign_word, english_word)] / sentence_total[foreign_word]
                total[english_word] += P[(foreign_word, english_word)] / sentence_total[foreign_word]

    # Estimate probabilities
    for english_word in english_words:
        for foreign_word in foreign_words:
            P[(foreign_word, english_word)] = tc[(foreign_word, english_word)] / total[english_word]

    if print_probabilities:
        print("--> P[('le','NULL')] =", P[('le', 'NULL')])
        print("--> P[('chien','NULL')] =", P[('chien', 'NULL')])
        print("--> P[('chat','NULL')] =", P[('chat', 'NULL')])
        print("--> P[('le','the')] =", P[('le', 'the')])
        print("--> P[('chien','the')] =", P[('chien', 'the')])
        print("--> P[('chat','the')] =", P[('chat', 'the')])
        print("--> P[('le','dog')] =", P[('le', 'dog')])
        print("--> P[('chien','dog')] =", P[('chien', 'dog')])
        print("--> P[('le','cat')] =", P[('le', 'cat')])
        print("--> P[('chat','cat')] =", P[('chat', 'cat')])
