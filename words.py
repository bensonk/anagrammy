#!/usr/bin/python
import os, readline, atexit, re
from pprint import pprint
histfile = os.path.join(os.environ["HOME"], ".words-history")
try: readline.read_history_file(histfile)
except IOError: pass
atexit.register(readline.write_history_file, histfile)

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
print "Done reading dictionary"

def print_words(words):
    for word in words:
        print word

lastwords = []
lastfind = ""
def find(letters, replace=False, count = 0):
  res = words.lookup(letters)
  if len(res) > count:
    res = res[-count:]
  print_words(res)
  if replace:
    global lastwords, lastfind
    lastwords = res
    lastfind = letters

def matcher(line, replace=False):
  global lastwords
  regex = re.compile(line)
  res = filter(lambda x: regex.findall(x), lastwords)
  if replace:
      lastwords = res
  print_words(res)

def process_line(line):
  if line.startswith("!"):
    line = line[1:]
    replace = True
  else:
    replace = False
  if not lastwords:
    replace = True

  if len(line) > 1:
    cmd, line = line[0], line[1:].strip()
  else:
    cmd = ""

  if " " in line: line, count = line.rsplit(" ", 1)
  else:           count = 0

  if cmd == ">":
    find(line.strip(), True, int(count))
  elif cmd == "+":
    find(line.strip() + lastfind, replace, int(count))
  elif cmd == "/":
    matcher(line, replace)
  else:
    print """Help:
  Commands:
    > [create]  Builds a word list based on supplied chars (e.g. > somecharstouse )  Follow with a number to limit results.
    + [add]     Builds new word list based on previous input with argument added (e.g. + foo)
    / [search]  Shows words that match regex (e.g. / ef$)
  Modifiers:
    ! [replace] Prepend to add or search to replace word list with result of command (e.g. !/ ^..s....$)
    """

if __name__ == "__main__":
  while True:
    try: process_line(raw_input(" ] "))
    except EOFError: break
print "" # To give the prompt back on its own line
