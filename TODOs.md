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
2. [X] Look into more phonetic algorithms
3. [X] Structure the project
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
10. [ ] Resize the node database to only store those phonetic codes that are needed
11. [ ] Add ways to configure it
12. [ ] Add a README.md
13. [ ] Create releases
  - Try learning github actions



# Current project
Structure the whole project

## Tasks
