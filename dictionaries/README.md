# Goals
1. A grammar **dictionary** with all words used
2. A **node database** with information about the node
3. A metaphone code for all node names 

# Todo
1. improve the grammar to sepparate words like uvshepre -> u v sphere
2. Improve the metaphone code (underscores change pronounciation)
3. clean up the amount of attributes the node list has
4. Implement the custom nodes in the funnystring-to-json.py file
5. Make it modular (make it have its own github repo: "resonite-node-database")
6. Include the node path (w/o the name) to the node list

# Key differences from funnystring.txt
1. Use of .json instead of a .txt separated by "|"s
2. Nodes have individual information (Name, Type, Metaphone)
3. Implementation of metaphone to perform metaphone searches