# Goals
1. [ ] Improving the phonetic search.
  - Value if it is worth adding a different kind of "type", an "underscore" type. Differentiating them from the "<type>".
  - Should not take the _ for calculating the metaphonetic code. There will never be a node called "Node_Type" and another "NodeType"
  - Evaluate wheter to add fuzzy search to the metaphone
2. [ ] Check the TODOs for the funnystring-to-json project
3. [ ] Add command recognition
  - Bind different aliases. ie: give me a, gimme a, generate a, create node, etc - type, of type, etc.
  - Must have a "type" identifier
    - When a type is specified, and the command uses types, return like: ValueAdd<float>
  - Mush have a "node-creation" command
  - When sending the commands to resonite, send identifiers instead (ie: new node, generate a, give me a -> NEWNODE)
5. [ ] Implement a web socked to communicate to Resonite
  - Check what others have made, perhaps.
  - Must be able to send the speech in text.
6. [ ] Create python tests
  - Record some of the more problematic nodes, and see how goot well they are being handled
7. [ ] Test under Windows
8. [ ] Check permormance on different bechmarks as well as in game (VR)
  - Note: the base model wasn't really that hard to run, but it's good to have numbers
  - since that may affect some people's decision
9. [ ] Add a README.md
10. [ ] Create releases
  - Try learning github actions


# Current project
1. Improving the phonetic search

## Current tasks
  - Value if it is worth adding a different kind of "type", an "underscore" type. Differentiating them from the "<type>".
  - Should not take the _ for calculating the metaphonetic code. There will never be a node called "Node_Type" and another "NodeType"
  - Evaluate whether to add fuzzy search to the metaphone
  - Revise all of the "not detected commands"
