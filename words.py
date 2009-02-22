#!/usr/bin/python
from pprint import pprint

class Wordstore(object):
  def __init__(self, file = None):
    if file: self.load(file)
    else: self.tree = dict()

  def _add_word(self, letters, tree):
    if letters:
      first = letters.pop(0)
      if first not in tree:
        tree[first] = dict()
      self._add_word(letters, tree[first])

  def add_word(self, word):
    self._add_word([ letter.lower().strip() for letter in word ], self.tree)

  def dump(self):
    pprint(self.tree)

  def load(self, filename):
    self.tree = dict()
    for word in open(filename).xreadlines():
      self.add_word(word)

  def lookup(self, letters):
    words = list(set(self._lookup(list(letters), self.tree, "")))
    words.sort(key = lambda x: len(x))
    return words

  def _lookup(self, letters, tree, string):
    ret = []
    if "" in tree: ret.append(string)
    if letters:
      for letter in letters:
        if letter in tree:
          new_letters = list(letters)
          new_letters.remove(letter)
          ret.extend(self._lookup(new_letters, tree[letter], string + letter))
    return ret

print "Reading dictionary..."
words = Wordstore("/usr/share/dict/words")
def find(letters, count = 00):
  res = words.lookup(letters)
  if len(res) > count:
    res = res[-count:]
  for word in res:
    print word
print "Done reading dictionary"
if __name__ == "__main__":
  while True:
    try: find(raw_input("> "))
    except: break
