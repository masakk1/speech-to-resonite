# Goals
1. [ ] Improving the phonetic search.
  - [X] Value if it is worth adding a different kind of "type", an "underscore" type. Differentiating them from the "<type>".
  NOTE: no
  - [X] Should not take the _ for calculating the metaphonetic code. There will never be a node called "Node_Type" and another "NodeType"
  - [X] Convert numbers to text when calculating metaphone code
  - [ ] Evaluate whether to add fuzzy search to the metaphone
  - [ ] Revise all of the "not detected commands"
  - [ ] fuzzy_search for phonetic_fuzz_search only searches for the nodes, return the whole node
  - [ ] Make use of metaphone1
2. [ ] Look into more phonetic algorithms
3. [ ] Structure the project
4. [ ] Check the TODOs for the funnystring-to-json project
5. [ ] Add command recognition
  - Bind different aliases. ie: give me a, gimme a, generate a, create node, etc - type, of type, etc.
  - Must have a "type" identifier
    - When a type is specified, and the command uses types, return like: ValueAdd<float>
  - Mush have a "node-creation" command
  - When sending the commands to resonite, send identifiers instead (ie: new node, generate a, give me a -> NEWNODE)
6. [ ] Implement a web socked to communicate to Resonite
  - Check what others have made, perhaps.
  - Must be able to send the speech in text.
7. [ ] Create python tests
  - Record some of the more problematic nodes, and see how goot well they are being handled
8. [ ] Test under Windows
9. [ ] Check permormance on different bechmarks as well as in game (VR)
  - Note: the base model wasn't really that hard to run, but it's good to have numbers
  - since that may affect some people's decision
10. [ ] Add a README.md
11. [ ] Create releases
  - Try learning github actions


# Current project
Looking into more phonetic algorithms

## Tasks
1. [ ] Create the phonetic algorithms - https://en.wikipedia.org/wiki/Phonetic_algorithm
  - [ ] Soundex
  - [ ] + fuzzy
  - [ ] Daitch–Mokotoff Soundex
  - [ ] + fuzzy
  - [ ] Cologne phonetics
  - [ ] + fuzzy
  - [ ] Metaphone and Double Metaphone (have a better search and utilise the metaphone1)
  - [ ] New York State Identification and Intelligence System
  - [ ] + fuzzy
  - [ ] Match Rating Approach 
  - [ ] + fuzzy
  - [ ] Caverphone
  - [ ] + fuzzy
2. [X] Add unit tests
  - [ ] make them more modular
3. [ ] add the "fuzzy" version of the metaphone as an option, not another function
4. [ ] Experiment with changing the theshold for fuzzy searches