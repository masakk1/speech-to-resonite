# Goals
1. [X] Improving the phonetic search.
  - [X] Value if it is worth adding a different kind of "type", an "underscore" type. Differentiating them from the "<type>".
  NOTE: no
  - [X] Should not take the _ for calculating the metaphonetic code. There will never be a node called "Node_Type" and another "NodeType"
  - [X] Convert numbers to text when calculating metaphone code
  - [X] Evaluate whether to add fuzzy search to the metaphone
  NOTE: no, it makes it worse somehow.
  - [ ] Revise all of the "not detected commands"
  - [X] Make use of metaphone1
  NOTE: after looking at other papers, the double metaphone was never better. (srhug)
2. [X] Look into more phonetic algorithms
3. [X] Structure the project
  - Modularised test
  - Modularised phonetic searches
  - Moved everything, basically
  - Added a main.py at the beginnign of the project
4. [X] Add the path for the nodes with the funnystring
5. [X] Add command recognition
  - [X] move config files out of the dictionaries
  - [X] Recognise starting commands 
  - [X] Recognise trailing commants
  - [X] Be able to add aliases to commants
  - [X] Send the commands with codes
  - [X] Write a list of the command_codes
6. [X] Implement a web socked to communicate to Resonite
  - Check what others have made, perhaps.
  - Must be able to send the speech in text.
7. [X] Create python tests
  - Record some of the more problematic nodes, and see how goot well they are being handled
8. [ ] Test under Windows
  - Creating it inside of resonite
9. [ ] Check permormance on different bechmarks as well as in game (VR)
  - Note: the base model wasn't really that hard to run, but it's good to have numbers
  - since that may affect some people's decision
10. [ ] Resize the node database to only store those phonetic codes that are needed
11. [ ] Add ways to configure it
12. [ ] Add a README.md
13. [ ] Create releases
  - Try learning github actions
14. [ ] Figure out how to seach for types



# Current project
Add commant recognition

## Tasks

