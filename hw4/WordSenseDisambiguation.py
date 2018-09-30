# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:03:49 2017

@author: Mohanakrishna
"""
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


def initialize(word):
    synset = wordnet.synsets(word)
    best_sense = ""
    synset_relations = dict()
    maxCount = 0
    for each in synset:
        synset_details = dict()
        count = each.lemmas()[0].count()
        synset_details["Count"] = count
        synset_details["Definition"] = word_tokenize(each.definition())
        examples = each.examples()
        example_words = list()
        for example in examples:
            example_words.extend(word_tokenize(example))
        synset_details["Examples"] = example_words
        synset_relations[each.name()] = synset_details
        if count > maxCount:
           best_sense = each
           maxCount = count
    return synset_relations, best_sense

def computeOverlap(signature, context):
    overlap = 0    
    for each_word in context:
        for each in signature:
            if str(each_word) == str(each):
                overlap += 1
                break
    return overlap

def simplifiedLesk(context, synset_relations, intialize_best_sense):
    best_sense = intialize_best_sense
    max_overlap = 0
    overlap_dict = dict()
    for sense, relations in synset_relations.items():
        signature = relations["Definition"]
        signature.extend(relations["Examples"])
        overlap = computeOverlap(signature, context)
        overlap_dict[sense] = overlap
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense
    return best_sense, overlap_dict

def main():
    sentence = "The bank can guarantee deposits will eventually cover future tuition costs because it invests in adjustable-rate mortgage securities."
    context = word_tokenize(sentence)
    synset_relations, intialize_best_sense = initialize("bank")
    best_sense, overlap = simplifiedLesk(context, synset_relations, intialize_best_sense)
    print("Best Sense:", best_sense)
    print('{:^50}'.format("SENSE"), '{:^50}'.format("OVERLAP"))
    for key in overlap:
        print('{:^50}'.format(key), '{:^50}'.format(overlap[key]))

if __name__== "__main__":
    main()
