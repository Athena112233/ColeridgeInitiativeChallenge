import nltk
from collections import Counter
import os, pickle, json, csv, copy


class Vocabulary(object):
    """Simple vocabulary wrapper."""

    def __init__(self):
        self.word2idx = {}
        self.idx2word = {}
        self.idx = 0

    def add_word(self, word):
        if not word in self.word2idx:
            self.word2idx[word] = self.idx
            self.idx2word[self.idx] = word
            self.idx += 1

    def __call__(self, word):
        if not word.lower() in self.word2idx:
            return self.word2idx['<unk>']
        return self.word2idx[word.lower()]

    def __len__(self):
        return len(self.word2idx)


def load_vocab(json, threshold):
    if os.path.isfile('savedVocab'):
        with open('savedVocab', 'rb') as savedVocab:
            vocab = pickle.load(savedVocab)
            print("Using the saved vocab.")

    else:
        vocab = build_vocab(json, threshold)
        with open('savedVocab', 'wb') as savedVocab:
            pickle.dump(vocab, savedVocab)
            print("Saved the vocab.")

    return vocab


def build_vocab(train_folder, threshold):
    train_files = os.listdir(train_folder)
    counter = Counter()
    for fname in train_files:
        with open(train_folder + fname) as f:
            sample_data = json.loads(f.read())
            for sec in sample_data:
                text = sec['text'].lower()
                tokens = nltk.tokenize.word_tokenize(text.lower())
                counter.update(tokens)


    # If the word frequency is less than 'threshold', then the word is discarded.
    words = [word for word, cnt in counter.items() if cnt >= threshold]

    # Create a vocab wrapper and add some special tokens.
    vocab = Vocabulary()
    vocab.add_word('<pad>')
    vocab.add_word('<start>')
    vocab.add_word('<end>')
    vocab.add_word('<unk>')

    #Add the words to the vocabulary.
    for i, word in enumerate(words):
        vocab.add_word(word)
    return vocab