import unittest
from autocomplete import AutoCompleteProvider, Candidate


class AutocompleteTestCase(unittest.TestCase):

    def test_single_recommendation(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
        matches = autocomplete.getWords('nee')
        self.assertEqual(matches, [
            Candidate(word='need', confidence=1)
        ])

    def test_multiple_recommendation_multiple_degrees(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train('need net')
        matches = autocomplete.getWords('ne')
        self.assertEqual(matches, [
            Candidate(word='need', confidence=1),
            Candidate(word='net', confidence=1)
        ])

    def test_case_insensitive_search(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train('need to')
        matches = autocomplete.getWords('NE')
        self.assertEqual(matches, [
            Candidate(word='need', confidence=1)
        ])

    def test_multiple_matches(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
        matches = autocomplete.getWords('thi')
        # "thing" (2), "think" (1), "third" (1), "this" (1)
        self.assertEqual(matches, [
            Candidate(word='thing', confidence=2),
            Candidate(word='think', confidence=1),
            Candidate(word='third', confidence=1),
            Candidate(word='this', confidence=1)
        ])

    def test_multiple_matches_multiple_weights(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
        matches = autocomplete.getWords('th')
        # "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
        self.assertEqual(matches, [
            Candidate(word='that', confidence=2),
            Candidate(word='thing', confidence=2),
            Candidate(word='the', confidence=1),
            Candidate(word='think', confidence=1),
            Candidate(word='third', confidence=1),
            Candidate(word='this', confidence=1),
            Candidate(word='thoroughly', confidence=1)
        ])

    def test_single_letter_word_detected(self):
        autocomplete = AutoCompleteProvider()
        autocomplete.train("I have a cat")
        matches = autocomplete.getWords('A')
        self.assertEqual(matches, [
            Candidate(word='a', confidence=1)
         ])
