from nltk.corpus import wordnet

def compute_overlap(signature, context):
    overlap = 0
    overlapWords = []
    for word in context:
        count = signature.count(word)
        if (count > 0):
            overlapWords.append(word)
            overlap += 1
    return (overlap, overlapWords)


def remove_stop_words(words):
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    return [word for word in words if word not in stop]


def simplifiedLESK(word, sentence, stopwords=False):
    synsets = wordnet.synsets(word)
    best_sense = synsets[0]
    max_overlap = 0
    context = sentence.split()
    if (stopwords):
        context = remove_stop_words(context)
    overlaps = {}
    for sense in synsets:
        signature = sense.definition().split()
        examples = sense.examples()
        for example in examples:
            signature += example.split()
        if (stopwords):
            signature = remove_stop_words(signature)
        overlap, overlapWords = compute_overlap(signature, context)
        overlaps[sense] = (overlap, overlapWords)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense
    return (best_sense, max_overlap, overlaps)


sentence = "The bank can guarantee deposits will eventually cover future tuition costs because it invests in adjustable-rate mortgage securities"
word = "bank"
stopwords = True;

selected_sence, max_overlap, overlaps = simplifiedLESK(word, sentence, stopwords)

for sense in overlaps:
    print("Sense\t\t\t: ", sense.name())
    print("Glossy\t\t\t: ", sense.definition())
    print("Total Overlaps\t: ", overlaps[sense][0])
    print("Overlap Words\t: ", overlaps[sense][1])
    print("\n")
print("Choosen Sense\t: ", selected_sence.name())
print("Glossy\t\t\t: ", selected_sence.definition())
print("Total Overlaps\t: ", overlaps[selected_sence][0])
print("Overlap Words\t: ", overlaps[selected_sence][1])
