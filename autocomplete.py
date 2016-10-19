from abc import ABCMeta, abstractmethod
import re
import string


class Candidate:
    def __init__(self, word, confidence=0):
        self.word = word
        self.confidence = confidence

    def getWord(self):
        return self.word

    def getConfidence(self):
        return self.confidence

    def __eq__(self, other):
        return (
            other.word == self.word
            and other.confidence == self.confidence
        )

    def __repr__(self):
        return "Candidate(word='{}', confidence={})".format(
            self.word, self.confidence)


class IWordStore(metaclass=ABCMeta):

    @abstractmethod
    def add(self, word):
        pass

    @abstractmethod
    def matches(self, fragment):
        """
        Returns a list of candidate instances matching the fragment.

        :param fragment:
        :return: [*Candidate()]
        """
        pass


class TrieWordStore(IWordStore):
    def __init__(self, value=None, children=None):
        self.value = value
        self.weight = 0
        self.children = {} if children is None else children

    def add(self, word):
        """
        Iterates through each letter in the word
        starting at the root node check to see if each letter is already
        represented in the trie

        If the letter is represented skip to the next letter
        If the letter is not represented create a new node and continue

        :param word:
        :return:
        """
        node = self
        for letter in word:
            if letter in node.children:
                node = node.children[letter]
            else:
                new_node = TrieWordStore(value=letter)
                node.children[letter] = new_node
                node = new_node

        # make sure to mark the last node as a word-end
        node.weight += 1

    def matches(self, fragment):
        node = self._get_fragment_node(fragment)
        if node is None:
            return []

        path = []
        words = {}

        self._walk_path(node, path, words)

        words = [
            Candidate(word=fragment + suffix, confidence=num_occurrences)
            for suffix, num_occurrences in words.items()
        ]
        return words

    def _get_fragment_node(self, fragment):
        """
        Returns the root node of the fragement, or None if no
        root node has been trained.

        :param fragment:
        :return: None/Node
        """
        node = self
        for letter in fragment:
            if letter in node.children:
                node = node.children[letter]
            else:
                return None
        return node

    def _walk_path(self, node, path, words):
        """
        Recursively walks all paths from a given node.

        Whenever a complete word is encountered the path is added to words
        :param node:
        :param path:
        :param words:
        :return:
        """
        if node.weight:
            words[''.join(n.value for n in path)] = node.weight

        for child in node.children.values():
            path.append(child)
            self._walk_path(child, path, words)

        if path:
            path.pop()

    def __repr__(self):
        return "TrieWordStore(value='{}', weight={}, children={})".format(
            self.value, self.weight, self.children)


class AutoCompleteProvider:

    def __init__(self):
        self.autocomplete = TrieWordStore()

    def getWords(self, fragment):
        """
        Searches for word matches based on fragment.
        Returns all matches as an array of Candidate instances
        Deldates to the autocomplete word store to find the matches.

        :param fragment:
        :return: [*Candidate]
        """
        # case insensitive search
        # and lowercase results
        fragment = fragment.lower()
        words = self.autocomplete.matches(fragment)
        return sorted(words, key=lambda x: (-x.confidence, x.word))

    def _build_word_str(self, fragment, path, letter):
        return fragment + ''.join([n.value for n in path]) + letter

    def _tokenize_words(self, passage):
        """
        Cleans a string of punctuation and splits on spaces.
        Returns a list of lowercase words.

        :param passage:
        :return:
        """
        return [s.lower() for s in
                re.sub('[' + string.punctuation + ']', '', passage).split()]

    def train(self, passage):
        """
        Tokenizes a string `passage`, naively and builds a trie
        for each word token.

        The autocomplete tree is stored with all lowercase letters.

        :param passage:
        :return:
        """
        words = self._tokenize_words(passage)

        for word in words:
            self.autocomplete.add(word)

