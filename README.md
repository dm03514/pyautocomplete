# pyautocomplete

Developed on:
```python
Python 3.5.2 (default, Jul 17 2016, 00:00:00)
[GCC 4.8.4] on linux
```

**Usage**

```python
$ ipython
Python 3.5.2 (default, Jul 17 2016, 00:00:00)
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: from autocomplete import AutoCompleteProvider

In [2]: ap = AutoCompleteProvider()

In [3]: f = open('/usr/share/dict/american-english')

In [4]: for word in f:
   ...:     ap.train(word)
   ...:

In [5]: ap.getWords('hi')
Out[5]:
[Candidate(word='hicks', confidence=3),
 Candidate(word='hibachis', confidence=2),
 Candidate(word='hiccoughs', confidence=2),
 Candidate(word='hiccups', confidence=2),
 Candidate(word='hickeys', confidence=2),
 ...
]
```

**Tests**

Tests should be self documenting.  Tests are writting using python `unittest` and
can be executed using:

```python
$ python -m unittest test_autocomplete
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

**Design**
The AutoCompleteProvider is a wrapper around a word store `IWordStore`.  For the
initial implementation a Trie was chosen.  To create a new implementation, implement
the `IWordStore` interface, which requires 2 methods:
- `void add(String word)` - adds a word to the word store
- `List<Candidate> matches(String fragement)` - returns all Candidate matches for a given fragment


We are developing a keyboard autocomplete algorithm to be used in various mobile devices. This algorithm will analyze the passages typed by the user in order to suggest a set of candidate autocomplete words given a word fragment.

We need you to write the algorithm that will learn the words typed by the user over time and then determine a ranked list of autocomplete candidates given a word fragment (you should ignore capitalization when providing suggestions). The algorithm will be trained in an online manner, meaning that additional training passages can be submitted and incorporated into the algorithm at the same time as the algorithm is being used to provide autocomplete suggestions. Ideally, the accuracy of the algorithm will improve over time as more and more training passages are incorporated. Due to the deployment environment for this algorithm, efficiency is critical. The data structure utilized by your algorithm should be optimized for space and time. We have provided a specification [1] and a sample passage [2] along with example input and output and would like you to provide the implementation.

[1] INTERFACE SPECIFICATION

Candidate
    String getWord() : returns the autocomplete candidate
    Integer getConfidence() : returns the confidence* for the candidate

AutocompleteProvider
    List<Candidate> getWords(String fragment) : returns list of candidates ordered by confidence*
    void train(String passage) : trains the algorithm with the provided passage
* Confidence is the likelihood/relevance of an individual word relative to the other words being returned by the autocomplete provider. If two words are equally likely, they should have the same confidence. If one is more likely, it should have a higher confidence.

[2] EXAMPLE WORDS AND THEIR EXPECTED NEXT WORDS BASED ON THE PROVIDED PASSAGES

Train: "The third thing that I need to tell you is that this thing does not think thoroughly."
Input: "thi" --> "thing" (2), "think" (1), "third" (1), "this" (1)
Input: "nee" --> "need" (1)
Input: "th" --> "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
