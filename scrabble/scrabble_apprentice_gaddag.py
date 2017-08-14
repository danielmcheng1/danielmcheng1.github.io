import os 
import _pickle as pickle
import string 

def write_gaddags_by_letter(scrabble_corpus):
    scrabble_corpus_by_letter = {letter: [] for letter in string.ascii_uppercase}
    for word in scrabble_corpus:
        scrabble_corpus_by_letter[word[0]].append(word)
    for letter in scrabble_corpus_by_letter:
        write_gaddag_for_one_letter(letter, scrabble_corpus_by_letter)
        
def write_gaddag_for_one_letter(letter, scrabble_corpus_by_letter):
    output_file = open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'gaddag_' + letter + '.txt'), 'wb')
    scrabble_gaddag = gaddag(scrabble_corpus_by_letter[letter], output_file)
    output_file.close()

def read_gaddag_by_letter(letter):
    input_file = open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'gaddag_' + letter + '.txt'), 'rb')
    return pickle.load(input_file)
    
    
   
#the hook represents where the prefix ends (up to and including the intersection tile)
GADDAG_HOOK = "@" 

#Gaddag naive implementation: 1820 megabytes for scrabble_gaddag
#partially compressed suffixes for a given word and eow letter sets: 854 mb!
#Execution time: 20-30 seconds for initial load
    
#global vars solely for printing (not for identifying)
GADDAG_PRINT_EOW = "."
GADDAG_PRINT_INDENT = "    "  
GADDAG_PRINT_ARROW = "-->"
class gaddag_node:
    def __init__(self):
        self.edges = dict()
        self.eow_set = set() 
        #a set tells us that we've reached the end of a word
        #we can use a set because any path leading to it is a word for any letter in that set
        #and any subsequent forced states share that same prefix (i.e. they are iterations of the same word)
      
    def add_eow(self, next_letter, eow_letter):
        if next_letter not in self.edges.keys():
            self.edges[next_letter] = gaddag_node()
        next_node = self.edges[next_letter]
        next_node.eow_set.add(eow_letter)
        return next_node
    
    def add_edge(self, next_letter):
        if next_letter not in self.edges.keys():
            self.edges[next_letter] = gaddag_node()
        return self.edges[next_letter]
    #If key is in the dictionary, return its value. 
    #If not, insert key with a value of default and return default. default defaults to None.
            #setdefault(key[, default])

    def force_edge(self, next_letter, forced_node):
        if next_letter in self.edges.keys() and not self.edges[next_letter] == forced_node:
            raise ValueError("Attempting to force an edge but an edge already exists to a different node for " + \
                             str(next_letter) + " to " + str(self.edges[next_letter].eow_set))
        self.edges[next_letter] = forced_node
        return self.edges[next_letter]
    
    def print_node(self, indent, path):
        node_edge_num = 0
        #either we've reached the end of a chain of nodes, 
        #or we can still continue on but we've reached an intermeidate eow set 
        if not self.edges or self.eow_set: 
            print (path + str(self.eow_set))
        for k in self.edges.keys():
            node_edge_num += 1
            if node_edge_num == 1:
                path = path + k + GADDAG_PRINT_ARROW
            else:
                path = indent + k + GADDAG_PRINT_ARROW
            self.edges[k].print_node(indent + GADDAG_PRINT_INDENT, path)
            
class gaddag:
    def __init__(self, corpus, output_file = None):
        self.start_node = gaddag_node()
        self.make_gaddag(corpus, output_file)
        
    def make_gaddag(self, corpus, output_file = None):
        for word in corpus:
            self.add_word(word)
        if output_file is not None:
            pickle.dump(self, output_file)
    def add_word(self, word):
        n = len(word)
        next_node = self.start_node
        for i in range(n - 1, 1, -1):
            next_node = next_node.add_edge(word[i])
        next_node = next_node.add_eow(word[1], word[0])
        #no need to add hook since no suffix exists
        next_node = self.start_node  
        
        for i in range(n - 2, -1, -1):
            next_node = next_node.add_edge(word[i])
        next_node = next_node.add_eow(GADDAG_HOOK, word[n-1])  
        
        for i in range(n - 3, -1, -1):
            forced_node = next_node
            next_node = self.start_node
            rev_prefix = word[i::-1]
            for letter in rev_prefix:
                next_node = next_node.add_edge(letter)
            next_node = next_node.add_edge(GADDAG_HOOK)
            next_node.force_edge(word[i+1], forced_node)   
            
    #for printing entire gaddag
    def print_gaddag(self):
        print("\n")
        self.start_node.print_node("", "")
    
    #for printing the paths for a list of consecutive letters (typically used to trace a prefix IN REVERSE)
    def print_select_gaddag_paths(self, start_letters):
        print("\n")
        start_path = ""
        start_indent = ""
        curr_node = self.start_node
        #we will try to find this full word in the Gaddag, which will appear as the reversed full prefix
        while len(start_letters):
            letter = start_letters.pop() #this traces the letters in reverse
            if letter in curr_node.edges.keys():
                if curr_node.eow_set:
                    print (start_path + str(curr_node.eow_set))
                start_path = start_path + letter + "-->"
                start_indent = start_indent + GADDAG_PRINT_INDENT
                curr_node = curr_node.edges[letter]
            elif not curr_node.edges or curr_node.eow_set: 
                if letter not in curr_node.eow_set:
                    print("Not in Gaddag")
                print (start_path + str(curr_node.eow_set))
                return
            else:
                print("Not in Gaddag")
                print(start_path + str(curr_node.eow_set))
                return
        curr_node.print_node(start_indent, start_path)
