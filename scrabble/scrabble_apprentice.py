#Author: Daniel M. Cheng
#Creation: February 2016
#Description: Scrabble AI based on Steven A. Gordon's GADDAG data structure (http://ericsink.com/downloads/faster-scrabble-gordon.pdf)
#Modified: July 2017 -- set up front-end server for playing against Scrabble AI 

import os, csv, sys, random

import scrabble_apprentice_gaddag 
#global gaddag so that this only loads once to server all requests 
SCRABBLE_APPRENTICE_GADDAG = scrabble_apprentice_gaddag.read_gaddag_full()

#coloring/config for original scrabble that printed out to console 
#import termcolor

'''
#function to grab the sizes of objects--useful for testing memory usage by GADDAG data structure
from pympler import asizeof
def get_size(obj):
    obj_size = sys.getsizeof(obj) / (1024 * 1024)

    print(str(obj_size) + " megabytes (sys)")
    obj_size = asizeof.asizeof(obj) / (1024 * 1024)

    print(str(obj_size) + " megabytes (pympler)")
    return obj_size
'''

#1: Loading scrabble score and frequency dictionaries, as well as bag and entire corpurs
#source lexicon: http://www.wordgamedictionary.com/twl06/download/twl06.txt
#the FreeScrabbleDictionary_twl06.txt, used for North American tournaments
#alternate lexicon: http://www.azspcs.net/Content/AlphabetCity/Lexicon.txt  
#minimum length for word in scrabble dictionary
MIN_WORD_LENGTH = 2
#load the corpus
def load_scrabble_corpus():
    scrabble_corpus= []
    #os.pardir to go back up a level
    with open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'FreeScrabbleDictionary_twl06.txt'), newline = '') as raw_corpus:
        for word in csv.reader(raw_corpus):
            cleaned_word = ''.join(word).upper()
            if len(cleaned_word) >= MIN_WORD_LENGTH: #this excludes 'A' and 'I'...for now...TBD
                scrabble_corpus.extend([cleaned_word])
    return scrabble_corpus

def load_scrabble_score_dict():
    scrabble_score_dict = dict()
    
    scrabble_score_dict[WILDCARD] = 0
    scrabble_score_dict['A'] = 1
    scrabble_score_dict['B'] = 3
    scrabble_score_dict['C'] = 3
    scrabble_score_dict['D'] = 2
    scrabble_score_dict['E'] = 1
    scrabble_score_dict['F'] = 4
    scrabble_score_dict['G'] = 2
    scrabble_score_dict['H'] = 4
    scrabble_score_dict['I'] = 1
    scrabble_score_dict['J'] = 8
    scrabble_score_dict['K'] = 5
    scrabble_score_dict['L'] = 1
    scrabble_score_dict['M'] = 3
    scrabble_score_dict['N'] = 1
    scrabble_score_dict['O'] = 1
    scrabble_score_dict['P'] = 3
    scrabble_score_dict['Q'] = 10
    scrabble_score_dict['R'] = 1
    scrabble_score_dict['S'] = 1
    scrabble_score_dict['T'] = 1
    scrabble_score_dict['U'] = 1
    scrabble_score_dict['V'] = 4
    scrabble_score_dict['W'] = 4
    scrabble_score_dict['X'] = 8
    scrabble_score_dict['Y'] = 4
    scrabble_score_dict['Z'] = 10
  
    return scrabble_score_dict
    

def load_scrabble_freq_dict():
    scrabble_freq_dict = dict()
    
    scrabble_freq_dict[WILDCARD] = 0
    scrabble_freq_dict['A'] = 9
    scrabble_freq_dict['B'] = 2
    scrabble_freq_dict['C'] = 2
    scrabble_freq_dict['D'] = 4
    scrabble_freq_dict['E'] = 12
    scrabble_freq_dict['F'] = 2
    scrabble_freq_dict['G'] = 3
    scrabble_freq_dict['H'] = 2
    scrabble_freq_dict['I'] = 9
    scrabble_freq_dict['J'] = 1
    scrabble_freq_dict['K'] = 1
    scrabble_freq_dict['L'] = 4
    scrabble_freq_dict['M'] = 2
    scrabble_freq_dict['N'] = 6
    scrabble_freq_dict['O'] = 8
    scrabble_freq_dict['P'] = 2
    scrabble_freq_dict['Q'] = 1
    scrabble_freq_dict['R'] = 6
    scrabble_freq_dict['S'] = 4
    scrabble_freq_dict['T'] = 6
    scrabble_freq_dict['U'] = 4
    scrabble_freq_dict['V'] = 2
    scrabble_freq_dict['W'] = 2
    scrabble_freq_dict['X'] = 1
    scrabble_freq_dict['Y'] = 2
    scrabble_freq_dict['Z'] = 1

    return scrabble_freq_dict

def load_scrabble_bag(scrabble_freq_dict):
    scrabble_bag = []
    for letter in scrabble_freq_dict.keys():
        scrabble_bag = scrabble_bag + [letter] * scrabble_freq_dict[letter]
    random.shuffle(scrabble_bag)
    return scrabble_bag

def load_all():
    scrabble_corpus = load_scrabble_corpus()
    scrabble_score_dict = load_scrabble_score_dict()
    scrabble_freq_dict = load_scrabble_freq_dict()
    scrabble_bag = load_scrabble_bag(scrabble_freq_dict)
    return (scrabble_score_dict, scrabble_freq_dict, scrabble_bag, scrabble_corpus)


        
#3: Scrabble board play class
#global vars
WILDCARD = ' ' #this are the two blank Scrabble tiles
HORIZONTAL = 1
VERTICAL = -1 #lose the benefit of boolean logic, but then you can multiply by -1 to flip
TRIPLE_LETTER = '3L'
TRIPLE_WORD = '3W'
DOUBLE_LETTER = '2L'
DOUBLE_WORD = '2W'
NO_BONUS = '  '
BINGO_BONUS = 50
RACK_MAX_NUM_TILES = 7
(MIN_ROW, MAX_ROW) = (0, 15)
(MIN_COL, MAX_COL) = (0, 15)
MAX_TURNS_PASSED = 6
(CENTER_ROW, CENTER_COL) = (7, 7)

FRONT_END = 1 #for checking if the spot before the first tile is filled
FRONT_OR_BACK_END = 2 #for checking if the spots before and after the word are filled

GEN_MOVES_PRINT_INDENT = "  "

#debugging/printing variables
DEBUG_PULL_VALID_CROSSWORD = False
DEBUG_GENERATE_MOVES = False
DEBUG_FINAL_CALC_SCORE = False
DEBUG_ALL_MOVES = False
'''
class apprentice:
    def __init__(board_obj):
        self.board_obj = board_obj
class board_config:
    def __init__():
'''    
#wrapper to replace scrabble_game.game_play method so that we can interface with flask/web app            
#change to be last move object separate....
def wrapper_play_next_move(data):
    print("Received data in scrabble_apprentice: {0}".format(str(data)))
    #initialize board 
    if data.get("scrabble_game_play", {}) == {}:
        print("initializing")
        (scrabble_score_dict, scrabble_freq_dict, scrabble_bag, scrabble_corpus) = load_all()
        scrabble_board = board(scrabble_bag, scrabble_score_dict, scrabble_corpus)
            
        human_player = scrabble_player("Human", IS_HUMAN, scrabble_board)  
        computer_player = scrabble_player("Computer", IS_COMPUTER, scrabble_board)  
        scrabble_game_play = game_play(scrabble_board, human_player, computer_player) 
        last_move_to_send = {"action": "Game Started", "player": "", "detail": ""}
        return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
    
    #otherwise read in the latest data and make the next move
    print("making human move")    
    scrabble_game_play = data["scrabble_game_play"]
    human_player = scrabble_game_play.play_order[0]
    computer_player = scrabble_game_play.play_order[1]
    scrabble_board = scrabble_game_play.board 
    last_move_to_send = {}
    
    #in case no data is passed through (e.g. relogging back into a session) 
    if data["scrabble_game_play_wrapper"]["last_move"] == {}:
        last_move_to_send = {"action": "Continuing Game from Previous Session", "player": "", "detail": ""}
        return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
    #make human move    
    if data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Passing":
        human_player.words_played.append({"word": list("PASSED"), "score": 0})
        last_move_to_send["player"] = "Human"
        last_move_to_send["action"] = "Passed"
        last_move_to_send["detail"] = ""           
    elif data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Exchanging Tiles":
        tiles_to_exchange = data["scrabble_game_play_wrapper"]["last_move"]["detail"]
        try:
            scrabble_game_play.exchange_tiles_during_turn(human_player, tiles_to_exchange) 
            human_player.words_played.append({"word": list("EXCHANGED"), "score": 0})
            last_move_to_send["player"] = "Human"
            last_move_to_send["action"] = "Exchanged Tiles"
            last_move_to_send["detail"] = ""
        except ValueError as e:
            log_illegal_move(last_move_to_send, e)
    elif data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Placing Tiles":
        tiles_to_place = data["scrabble_game_play_wrapper"]["last_move"]["detail"]
        try: 
            full_placement = scrabble_board.convert_placed_tiles_to_full_placement(tiles_to_place)
            score = scrabble_board.make_human_move(full_placement["start_row"], full_placement["start_col"], full_placement["direction"], full_placement["word"], human_player)
            last_move_to_send["player"] = "Human"
            last_move_to_send["action"] = "Placed Tiles"
            last_move_to_send["detail"] = full_placement["word"] 
            wrapper_end_turn(human_player, full_placement["word"], score, scrabble_game_play)
        except ValueError as e:   
            log_illegal_move(last_move_to_send, e)
            
    print("last move:", last_move_to_send["action"]);
    if last_move_to_send["action"] != "Made Illegal Move":
        #increment for human passing 
        increment_turns_passed(scrabble_game_play, last_move_to_send)
        print("num turns passed: {0}".format(scrabble_game_play.num_turns_passed))
           
        print("Game has ended: {0}, game end reason: {1}".format(scrabble_game_play.game_has_ended(), scrabble_game_play.game_end_reason()))
        if scrabble_game_play.game_has_ended():
            return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
            
        #make computer move 
        print("Computer move")
        (score, word) = scrabble_game_play.board.make_computer_move(computer_player)     
        #if the computer is unable to find a move, exchange tiles
        print("score: {0}, word {1}".format(score, str(word)))
        if word == []:
            try: 
                scrabble_game_play.exchange_tiles_during_turn_capped(computer_player, computer_player.rack)
                last_move_to_send["action"] = "Exchanged Tiles"
                human_player.words_played.append({"word": list("EXCHANGED"), "score": 0})
            except ValueError as e:
                last_move_to_send["action"] = "Passed"
                human_player.words_played.append({"word": list("PASSED"), "score": 0})
            last_move_to_send["player"] = "Computer"
            last_move_to_send["detail"] = "" #could return tiles exchanged instead
        else: 
            last_move_to_send["player"] = "Computer"
            last_move_to_send["action"] = "Placed Tiles" 
            last_move_to_send["detail"] = word
            wrapper_end_turn(computer_player, word, score, scrabble_game_play)
        increment_turns_passed(scrabble_game_play, last_move_to_send)
    return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
def wrapper_save_game_play(scrabble_game_play, last_move_to_send):   
    print("wrapping") 
    human_player = scrabble_game_play.play_order[0]
    computer_player = scrabble_game_play.play_order[1]
    scrabble_board = scrabble_game_play.board
    scrabble_score_dict = scrabble_board.scrabble_score_dict
    
    scrabble_game_play_wrapper = {"board": [[map_cell_to_bonus_view(scrabble_board.board[row][col]) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "tiles": [[map_cell_to_tile_view(scrabble_board.board[row][col], map_cell_to_player_view(row, col, scrabble_board), scrabble_score_dict) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "rackHuman": map_rack_to_tile_view(human_player.rack, "Human", scrabble_score_dict),   \
                              "rackComputer": map_rack_to_tile_view(computer_player.rack, "Computer", scrabble_score_dict), \
                              "gameInfo": {"scoreHuman": human_player.running_score, "scoreComputer": computer_player.running_score,
                                           "wordsPlayedHuman": human_player.words_played, "wordsPlayedComputer": computer_player.words_played,
                                           "tilesLeft": len(scrabble_board.bag),
                                           "gameEndReason": scrabble_game_play.game_end_reason()}, \
                              "lastMove": last_move_to_send
                              }
                              
    return {"scrabble_game_play_wrapper": scrabble_game_play_wrapper, "scrabble_game_play": scrabble_game_play}

def wrapper_end_turn(player, word, score, game_play):
    player.words_played.append({"word": word, "score": score})
    player.running_score += score   
    game_play.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES - len(player.rack)) 
    
def increment_turns_passed(scrabble_game_play, move):
    if move["action"] == "Passed":
        scrabble_game_play.num_turns_passed += 1
    else:
        scrabble_game_play.num_turns_passed = 0 
        
def log_illegal_move(last_move_to_send, e):
    last_move_to_send["player"] = "Human"
    last_move_to_send["action"] = "Made Illegal Move" 
    last_move_to_send["detail"] = "".join(e.args)
    
def map_cell_to_bonus_view(cell):
    if cell == TRIPLE_LETTER:
        return 'Triple Letter'
    if cell == TRIPLE_WORD:
        return 'Triple Word'
    if cell == DOUBLE_LETTER:
        return 'Double Letter'
    if cell == DOUBLE_WORD:
        return 'Double Word'
    if cell == NO_BONUS:
        return ''
    #TBD have to see if bonusess get replaced by letters 
    #print('WARNING: returning blank for {0}'.format(cell))
    return ''
    
def map_cell_to_tile_view(cell, player_type, scrabble_score_dict):
    #TBD flip to the is_scrabble_tile method? 
    #TBD player type vs. player vs. player name
    #cell is actually a tile...
    if cell.isalpha():
        return tile(cell, player_type, scrabble_score_dict).get_tile()
    return ''
    
def map_cell_to_player_view(row, col, scrabble_board):
    return scrabble_board.board_to_player[row][col]

def map_rack_to_tile_view(rack, player_type, scrabble_score_dict):
    return [tile(letter, player_type, scrabble_score_dict).get_tile() for letter in rack]
        
#TBD player name, type, or ID?    
class tile:
    def __init__(self, letter, player_type, scrabble_score_dict):
        self.letter = letter
        self.player_type = player_type
        self.points = scrabble_score_dict[letter] 
        
    def get_tile(self):
        return {'letter': self.letter, 'points': self.points, 'player_type': self.player_type}
        
class board:
    #highest for loop appears first!! http://rhodesmill.org/brandon/2009/nested-comprehensions/
    def __init__(self, bag, score_dict, corpus):
        self.board = [[self.add_premium(row, col) for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        self.board_to_player = [["" for col in range(MIN_COL, MAX_COL)] for row in range(MIN_ROW, MAX_ROW)]
        self.num_words_placed = 0
        self.bag = bag
        self.scrabble_score_dict = score_dict
        self.scrabble_corpus = corpus
        
    def clear_comp(self):
        self.comp_max_score = 0
        self.comp_max_word = []
        self.comp_max_row = None
        self.comp_max_col = None
        self.comp_max_direction = None
        self.comp_all_possible_moves = {HORIZONTAL:{}, VERTICAL:{}}
        
    def add_premium(self, row, col):
        if not (row % 7) and not (col % 7) and not (row == 7 and col == 7):
            return TRIPLE_WORD
        elif row + col == 14 or row == col:
            if row in (5, 9):
                return TRIPLE_LETTER
            elif row in (6, 8):
                return DOUBLE_LETTER
            else:
                return DOUBLE_WORD
        elif (row, col) in ((0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,12),(7,3),(7,11),(8,2),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)):
            return DOUBLE_LETTER
        elif (row, col) in ((1,5),(1,9),(5,1),(5,13),(9,1),(9,13),(13,5),(13,9)):
            return TRIPLE_LETTER
        else:
            return NO_BONUS
    
    #TBD only print every other
    #http://thelivingpearl.com/2012/12/28/playing-around-with-strings-and-python/
    #https://pypi.python.org/pypi/termcolor
    #http://stackoverflow.com/questions/22104920/how-do-i-print-a-grid-from-a-list-of-lists-with-numbered-rows-and-columns
    #0:02d to pad with zero, if col else "  " for ignoring 0
    '''
    def print_board(self):  
        labels_to_print = [0, 3, 7, 11, 14]   
        print()
        print("  " + " ".join("{0:2d}".format(col) for col in range(MIN_COL, MAX_COL)))
        for row_num, row in enumerate(self.board, 0):
            #if row_num in labels_to_print:
            print("{0:2d}".format(row_num), end = "|")
            for cell in row:
                #row_cleaned = [self.print_board_cleaner(cell) for cell in row]
                (cell_cleaned, cell_color) = self.print_board_color_cleaner(cell)
                print(termcolor.colored(cell_cleaned, cell_color), end="|")
            print("")
    '''
        
    def print_board_color_cleaner(self, cell):
        if cell.isalpha():
            cell_cleaned = cell + " "
            cell_color = "green"
        else:
            cell_cleaned = cell
            if cell == TRIPLE_LETTER:
                cell_color = "blue"
            elif cell ==  DOUBLE_LETTER:
                cell_color = "blue"
            elif cell == TRIPLE_WORD:
                cell_color = "red"
            elif cell == DOUBLE_WORD:
                cell_color = "red"
            else:
                cell_color = "grey"
        return (cell_cleaned, cell_color)
    
    def print_max_move(self):
        if board.comp_max_direction == HORIZONTAL:
            direction = " going horizontally"
        else:
            direction = " going vertically"
        print("\nAnd the optimal move is...")
        print("***Drumroll***")
        print(''.join(self.comp_max_word) + " worth " + str(self.comp_max_score) + " pts at " + \
              str((board.comp_max_row, board.comp_max_col)) + direction)
    
    #TBD: false for beyond boudnaries seems dangerous
    def is_scrabble_tile(self, row, col):
        #went beyond bounds of board--useful when checking valid anchor squares and whether the ends are filled
        #we have to make this explicit or else board[-1] will wrap around!!
        if row < MIN_ROW or col < MIN_COL or row >= MAX_ROW or col >= MAX_COL:
            return False
        elif self.board[row][col].isalpha():
            return True
        else:
            return False
        
    def is_valid_word(self, word):
        return "".join(word) in self.scrabble_corpus 
        '''
        curr_node = self.gaddag.start_node
        #reverse because the full word is stored as a reveresed prefix in the Gaddag
        word_reversed = word[::-1] #this is a shallow copy, but the letters in this list are not mutable
        for pos, letter in enumerate(word_reversed, 0):
            #if we're at the last letter, this is a valid word iff it is part of the eow_set
            if pos == len(word_reversed) - 1:
                #print("in eow test for letter: " + letter + " at pos: " + str(pos))
                if letter in curr_node.eow_set:
                    return True
                else:
                    return False
            #if we aren't at the last letter, try to move to the next node in the gaddag
            elif letter in curr_node.edges.keys():
                curr_node = curr_node.edges[letter]
                #print("in edges for letter: " + letter + " at pos: " + str(pos))
            #if we can't move to a next node, then this is not a valid word in our Scrabble dictionary
            else:
                #print("did not find edge for letter: " + letter + " at pos: " + str(pos))
                return False
        #this could happen if we pass a null word into this function
        return False
        '''
                
    #exception for the first move
    def intersect_center_tile(self, start_row, start_col, direction, word):
        if direction == HORIZONTAL:
            if start_row != 7 or start_col > CENTER_COL or start_col + len(word) - 1 < CENTER_COL:
                return False
        else:
            if start_col != 7 or start_row > CENTER_ROW or start_row + len(word) - 1 < CENTER_ROW:
                return False
        return True
    #this places the word on the board 
    #(this is called at the end of the move sequence...seems silly to abort NOW, but TBD if this can be improved)
    #e.g. two of the checks below can be moved out at least to the beginning of the move
        #...and maybe checking if is a word
    def place_word(self, start_row, start_col, direction, word, player):
        num_tiles = len(word) 
        if direction == HORIZONTAL:
            end_row = start_row + 1
            end_col = start_col + num_tiles
        else:
            end_row = start_row + num_tiles
            end_col = start_col + 1
            
        #check that these tiles fit the board
        if (start_row < MIN_ROW or start_col < MIN_COL) or (end_row > MAX_ROW or end_col > MAX_COL) :
            raise ValueError('Word does not fit on the board')
        if num_tiles < MIN_WORD_LENGTH:
            raise ValueError('Word is too short. The minimum word length is ' + str(MIN_WORD_LENGTH) + " letters")
            
        #place in this given row or col, 
        #but break if you overlap an existing tile (and your input letters do not match up with those tiles)
        (saved_row, saved_col) = (self.board[start_row][:], self.board[:][start_col])
        for curr_row in range(start_row, end_row):
            for curr_col in range(start_col, end_col):
                to_place = word[curr_row - start_row + curr_col - start_col] #the extra blank padding only appears when printing
                if not to_place.isalpha():
                    (self.board[start_row][:], self.board[:][start_col]) = (saved_row, saved_col) 
                    raise ValueError('Please place only letters on the board')
                if self.is_scrabble_tile(curr_row, curr_col) and self.board[curr_row][curr_col] != to_place:
                    (self.board[start_row][:], self.board[:][start_col]) = (saved_row, saved_col) 
                    raise ValueError('Your tile {0} overlaps existing tiles on the board (perhaps from a concurrent session?)'.format(to_place))
                #remove from rack and place if this isn't an existing tile on the board
                if self.board[curr_row][curr_col] != to_place:
                    self.board[curr_row][curr_col] = to_place
                    player.rack.remove(to_place)
                    self.board_to_player[curr_row][curr_col] = player.name #stamp tile with this player's name
        self.num_words_placed += 1
        
    #http://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand12/Group3Johan/report/berntsson_ericsson_report.pdf example scoring
    #calculate score--compute score for a given word off of the "real" board to calculate bonsues
        #hence this does not affect the shadow board, nor does it touch the real board aside from pulling bonuses
        #this allows us to abstract out the calc score function for computing both crosswords and regular words,
        #and allows ut to correctly compute bonuses for overlapping crosswords and regular words
    #valid_crossword_score_dict is a cache of the crossword scores for that spot
        #if it is empty, then there are no crosswords to compute
        #hence, when pull_valid_crossword_score calls this function, it passes an empty dictionary
    #we ask for the word and calculate scores based on this (instead of walking over the board) 
        #because this allows us to remember bonuses (ehhh not really...you could always undo)                           
    def calc_word_score(self, start_row, start_col, direction, word, valid_crossword_score_dict):
        
        num_tiles = len(word) #to set boundaries
        num_tiles_used = 0 #to keep track of bingo score
                               
        crossword_scores = 0 #to keep track of ALL crossword scores
        total_score = 0 #running total score
        word_multiplier = 1 #overall word multiplier
        letter_multiplier = 1 #individual tile multipliers
        
        #set boundaries
        if direction == HORIZONTAL:
            end_row = start_row + 1
            end_col = start_col + num_tiles
        else:
            end_row = start_row + num_tiles
            end_col = start_col + 1
                               
        #increment over the word while checking the bonus values on the real board (NO PLACEMENT IS DONE)                  
        for curr_row in range(start_row, end_row):
            for curr_col in range(start_col, end_col):
                #if we aren't overlapping an existing tile, then increment the tile count
                if not self.is_scrabble_tile(curr_row, curr_col):
                    num_tiles_used = num_tiles_used + 1
                
                #calculate score and bonus for this letter
                curr_letter = word[curr_row - start_row + curr_col - start_col]
                curr_bonus = self.board[curr_row][curr_col]
                
                if curr_bonus == TRIPLE_LETTER:
                    letter_multiplier = 3
                elif curr_bonus == DOUBLE_LETTER:
                    letter_multiplier = 2
                elif curr_bonus == TRIPLE_WORD:
                    word_multiplier *= 3
                elif curr_bonus == DOUBLE_WORD:
                    word_multiplier *= 2
                else:
                    curr_bonus = NO_BONUS #technically includes letter tiles--can remove this when printing is no longer done
                               
                total_score += letter_multiplier * self.scrabble_score_dict[curr_letter]
                letter_multiplier = 1
        
                #add in crossword score
                if valid_crossword_score_dict:
                    if (curr_row, curr_col) in valid_crossword_score_dict.keys():
                        #this letter should always exist as a key since we precalculated all crossword combinations
                        crossword_scores += valid_crossword_score_dict[(curr_row, curr_col)][curr_letter]                  
                #http://blog.lerner.co.il/calculating-scrabble-scores-reduce/ 
                #reduce(lambda total, current: total + points[current], word, 0)
                
                #TBD printing for debugging
                if valid_crossword_score_dict and DEBUG_PULL_VALID_CROSSWORD:
                    print(str(curr_letter) + ": " + str(self.scrabble_score_dict[curr_letter]) + "pts" + \
                      " --> bonus : " + str(curr_bonus) + " pts at " + str(curr_row) + "," + str(curr_col))                                  
                elif DEBUG_PULL_VALID_CROSSWORD:
                    print("\t" + str(curr_letter) + ": " + str(self.scrabble_score_dict[curr_letter]) + "pts" + \
                      " --> bonus : " + str(curr_bonus) + " pts at " + str(curr_row) + "," + str(curr_col))                                  
                
        #final word multiplier bonus
        total_score *= word_multiplier
        if not valid_crossword_score_dict and DEBUG_PULL_VALID_CROSSWORD:
            print("Word multiplier: " + str(word_multiplier) + " --> Total score: " + str(total_score) + " pts")
        elif DEBUG_PULL_VALID_CROSSWORD:
            print("\tWord multiplier: " + str(word_multiplier) + " --> Total score: " + str(total_score) + " pts")
        
        #add in crossword scores and bingo scores
        total_score += crossword_scores
        if valid_crossword_score_dict and num_tiles_used == RACK_MAX_NUM_TILES:
            total_score += BINGO_BONUS
            if DEBUG_PULL_VALID_CROSSWORD:
                print("Bingo bonus of: " + str(BINGO_BONUS) + " pts")
        
        if DEBUG_PULL_VALID_CROSSWORD:
            print("Final score: " + str(total_score) + " pts")
        return total_score
   
    #checks if there is a valid crossword orthogonal to the original tile
    #returns a score of -1 if there the input letter creates an invalid crossword, 
    #a score of 0 if there is no crossword (so any tile is OK)
    #and a 1+ score if there is a valid crossword
    def pull_valid_crossword_score(self, orig_letter, orig_row, orig_col, orig_direction):
        #saved_tile = self.board[orig_row][orig_col]
        #self.board[orig_row][orig_col] = orig_letter
                               
        #if not self.is_scrabble_tile(self.shadow_board, orig_row, orig_col):
        #    raise ValueError('Attempted to calculate crossword at a non-letter tile: ' + 
        #                    str(self.shadow_board[orig_row][orig_col]) + " " + str(orig_row) + ", " + str(orig_col))
        #crossword.append(self.board[orig_row][orig_col])
        #if a tile already exists there, we do not need to check crosswords--
        #--because this tile has already been placed, and its crossword validated/scored in a previous move
        if self.is_scrabble_tile(orig_row, orig_col):
            crossword_score = -1
            if DEBUG_PULL_VALID_CROSSWORD:
                print("Existing tile already; no need to calculate crossword")
            return crossword_score
        crossword = []
        crossword.append(orig_letter)

        #first find the beginning of the word
        (curr_row, curr_col) = (orig_row, orig_col)
        if orig_direction == HORIZONTAL:
            (row_delta, col_delta) = (-1, 0)
        else:
            (row_delta, col_delta) = (0, -1)
        while True:
            (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
            if curr_row >= MIN_ROW and curr_col >= MIN_COL and self.is_scrabble_tile(curr_row, curr_col):
                crossword.insert(0, self.board[curr_row][curr_col]) #insert in front
            else:
                break
                
        #save the beginning row/col
        crossword_start_row = curr_row - row_delta #undo the most recent delta operation that caused the loop break
        crossword_start_col = curr_col - col_delta
        
        #reset and find the end of the word
        (curr_row, curr_col) = (orig_row, orig_col)
        (row_delta, col_delta) = (row_delta * -1, col_delta * -1)
        while True:
            (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
            if curr_row < MAX_ROW and curr_col < MAX_COL and self.is_scrabble_tile(curr_row, curr_col):
                crossword.append(self.board[curr_row][curr_col]) #append to end
            else:
                break  
        
        #TBD: better method...
        #crossword = ''.join([letter.strip() for letter in crossword_list])
        if DEBUG_PULL_VALID_CROSSWORD:
            print(crossword)
        #no crosswords were formed, so it is ok to place this tile here
        if len(crossword) == 1:
            crossword_score = 0 
        #we formed a valid crossword-->calculate the score!
        elif self.is_valid_word(crossword):
            if DEBUG_PULL_VALID_CROSSWORD:
                print("\tCrossword is: " + str(crossword) + " located at " + str(crossword_start_row) + ", " + str(crossword_start_col))
            crossword_score = self.calc_word_score (crossword_start_row, crossword_start_col, \
                                                          -1 * orig_direction, crossword, {})
        #we formed an invalid crossword
        else:
            crossword_score = -1  
        
        if DEBUG_PULL_VALID_CROSSWORD:
            print("\tCrossword score is: " + str(crossword_score) + " pts")
        return crossword_score
        
    #TBD: do I need to copy shadow board?
    #TBD: dangerous to mix functions?
    #--which ones are OK with invalid words? (crossword_score function vs. find_valid_cross_spots)
     
    def pull_spot_to_valid_crossword_score(self, orig_row, orig_col, orig_direction, \
                                            valid_crossword_score_dict, rack):
        #saved_shadow_tile = self.shadow_board[orig_row][orig_col]
        #dedupe the rack since we shouldn't compute the score for the same letter twice
        rack_uniq = set(rack)
        #TBD: if blank, then just compute all alphabetic letters
        for letter in rack_uniq:
            #self.shadow_board[orig_row][orig_col] = letter
            crossword_score = self.pull_valid_crossword_score(letter, orig_row, orig_col, orig_direction)
            #score of negative one means crossword is invalid
            if crossword_score != -1:
                if (orig_row, orig_col) in valid_crossword_score_dict.keys():
                    if letter in valid_crossword_score_dict.keys():
                        raise ValueError("Found a duplicate in crossword score dict")
                    valid_crossword_score_dict[(orig_row, orig_col)][letter] = crossword_score
                else:
                    valid_crossword_score_dict[(orig_row, orig_col)] = {}
                    valid_crossword_score_dict[(orig_row, orig_col)][letter] = crossword_score
                    
        #reset this tile back to the original value
        #self.shadow_board[orig_row][orig_col] = saved_shadow_tile
    def pull_valid_hook_spot(self, row, col, valid_hook_spots):
        #if this is the first word placed on the board, it must start left of or above of the center spot
        if self.num_words_placed == 0:
            if row <= CENTER_ROW and col <= CENTER_COL:
                valid_hook_spots.append((row, col))
        #check if this is a blank spot 
        elif not self.is_scrabble_tile(row, col):
            #check if there is a non-blank spot on the board adjacent to it
            #TBD: is_scrabble_tile returns false if we go out of bounds...
            if self.is_scrabble_tile(row - 1, col) or \
            self.is_scrabble_tile(row + 1, col) or \
            self.is_scrabble_tile(row, col - 1) or \
            self.is_scrabble_tile(row, col + 1):                          
                valid_hook_spots.append((row, col))   
                #elif self.is_scrabble_tile(self.board, curr_row, curr_col) and \
                #((orig_direction == HORIZONTAL and self.is_empty_tile(self.board, curr_row, curr_col + 1)) or \
                #(orig_direction == VERTICAL and self.is_empty_tile(self.board, curr_row + 1, curr_col))):
                #    valid_starting_hook_spots.extend((curr_row, curr_col))

    #given a direction (horizontal or vertical) and rack of tiles, 
    #this function finds all "hook"/anchor spots that we can place words at
    #this function also creates a mapping from each spot in that row/col to all valid crosswords
        #these are the crosswords orthogonal to the desired direction 
        #(e.g. I want to place horizontally-->which words allow for valid vertical crosswords?)
    def pull_hooks_and_crosswords(self, start_row, start_col, direction, rack):
        if direction == HORIZONTAL:
            (end_row, end_col) = (start_row + 1, MAX_COL)
        else:
            (end_row, end_col) = (MAX_ROW, start_col + 1)
        
        valid_hook_spots = []
        valid_crossword_score_dict = {} 
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if DEBUG_PULL_VALID_CROSSWORD:
                    print("(Row, Col): "+ str((row, col)))
                self.pull_valid_hook_spot(row, col, valid_hook_spots)              
                self.pull_spot_to_valid_crossword_score(row, col, direction, valid_crossword_score_dict, rack)  
                if DEBUG_PULL_VALID_CROSSWORD:
                    print(valid_hook_spots)
                    print(valid_crossword_score_dict)
                
   
        return (valid_hook_spots, valid_crossword_score_dict)
 
    def find_coordinate_bounds_of_word(self, curr_offset, hook_row, hook_col, direction, word):
        if direction == HORIZONTAL:
            #either we were offset to the beginning of the word (i.e. we hit eow on a reversed prefix)
            if curr_offset <= 0:
                (start_row, start_col) = (hook_row, hook_col + curr_offset)
            #or we were offset to the end of the word
            else:
                (start_row, start_col) = (hook_row, hook_col + curr_offset - len(word) + 1)
            (end_row, end_col) = (start_row, start_col + len(word) - 1)
        else:
            if curr_offset <= 0:
                (start_row, start_col) = (hook_row + curr_offset, hook_col)
            else:
                (start_row, start_col) = (hook_row + curr_offset - len(word) + 1, hook_col)
            (end_row, end_col) = (start_row + len(word) - 1, start_col)
        return (start_row, start_col, end_row, end_col)
       
    #checks that if we continue to concatenate, 
        #that there is NOT a tile to the left (above) or to the right (below) of this eow
    def ends_are_filled(self, curr_offset, hook_row, hook_col, direction, word, front_or_back):
        (start_row, start_col, end_row, end_col) = \
            self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
        #print(word)
        #print(str((start_row, start_col, end_row, end_col)))
        if direction == HORIZONTAL:
            (front_row, front_col) = (start_row, start_col - 1)
            (back_row, back_col) = (end_row, end_col + 1)
        else:
            (front_row, front_col) = (start_row - 1, start_col)
            (back_row, back_col) = (end_row + 1, end_col)
        if front_or_back == FRONT_END:
            return self.is_scrabble_tile(front_row, front_col)
        elif front_or_back == FRONT_OR_BACK_END:
            return self.is_scrabble_tile(front_row, front_col) or self.is_scrabble_tile(back_row, back_col)
        else:
            raise ValueError("Requested something besides FRONT_END or FRONT_OR_BACK_END")
    
    #this is called once we hit the end of a word     
    def save_word_and_score(self, curr_offset, hook_row, hook_col, direction, word, valid_crossword_score_dict, indent):
        (start_row, start_col, end_row, end_col) = self.find_coordinate_bounds_of_word(curr_offset, hook_row, hook_col, direction, word)
        
        if DEBUG_FINAL_CALC_SCORE:
            global DEBUG_PULL_VALID_CROSSWORD
            save_user_option = DEBUG_PULL_VALID_CROSSWORD
            DEBUG_PULL_VALID_CROSSWORD = True
            word_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
            DEBUG_PULL_VALID_CROSSWORD = save_user_option
        word_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
        #exception for the first move
        if self.num_words_placed == 0 and not self.intersect_center_tile(start_row, start_col, direction, word):
            return
        
            
        cleaned_word = ''.join(word) #make this a string for ease of reading--this dictionary isn't used for anything aside from debugging
        if (start_row, start_col) in self.comp_all_possible_moves[direction].keys():
            if cleaned_word in self.comp_all_possible_moves[direction][(start_row, start_col)].keys():
                #TBD--overlap between col and row iterations
                print(cleaned_word + " at " + str((start_row, start_col)) + " with score " + str(word_score))
                print(self.comp_all_possible_moves)
                raise ValueError("Resaving a word that was previously computer calculated with a different score")
            self.comp_all_possible_moves[direction][(start_row, start_col)][cleaned_word] = word_score
        else:
            self.comp_all_possible_moves[direction][(start_row, start_col)] = {}
            self.comp_all_possible_moves[direction][(start_row, start_col)][cleaned_word] = word_score
            
        if word_score > self.comp_max_score:
            self.comp_max_score = word_score
            self.comp_max_word = word #save this as a list since this is the standard type throughout
            self.comp_max_row = start_row
            self.comp_max_col = start_col
            self.comp_max_direction = direction
        if DEBUG_GENERATE_MOVES:
            print(indent + GEN_MOVES_PRINT_INDENT + "SAVED THIS WORD: " + cleaned_word + " at " + str((start_row, start_col)))
  

    #tries to concatenate the input letter onto the prefix or suffix of the word    
    def concatenate_next(self, letter, curr_node, curr_rack, curr_word,
                       curr_offset, hook_row, hook_col, direction, boundary,
                       valid_crossword_score_dict, indent):
        #if we've reached an ending node, save this word (for both prefix and suffix b/c the prefix could be the WHOLE word)
        if letter in curr_node.eow_set:
            if curr_offset <= 0:
                completed_word = [letter] + curr_word
            else:
                completed_word = curr_word + [letter]
            if not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, completed_word, FRONT_OR_BACK_END):
                if DEBUG_GENERATE_MOVES:
                    print(indent + "reached an eow: " + str(completed_word))
                self.save_word_and_score(curr_offset, hook_row, hook_col, direction, completed_word, 
                                           valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT) 
        #placing prefix
        if curr_offset <= 0:
            if letter in curr_node.edges.keys():
                curr_node = curr_node.edges[letter]
                new_word = [letter] + curr_word
                if DEBUG_GENERATE_MOVES:
                    print(indent + "building up prefix: " + str(new_word) + " with rack " + str(curr_rack))
                self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    curr_offset - 1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
                #if the next node leads to a hook, then we have to reverse 
                #(unless we're bumping up against another tile on the board)
                if scrabble_apprentice_gaddag.GADDAG_HOOK in curr_node.edges.keys() and \
                not self.ends_are_filled(curr_offset, hook_row, hook_col, direction, new_word, FRONT_END):
                    curr_node = curr_node.edges[scrabble_apprentice_gaddag.GADDAG_HOOK]
                    if DEBUG_GENERATE_MOVES:
                        print(indent + "found a hook-->reversing now with: " + str(new_word) + " with rack " + str(curr_rack))
                    self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
            elif DEBUG_GENERATE_MOVES:
                print (indent + "unable to continue building prefix")
        #placing suffix
        else:      
            if letter in curr_node.edges.keys():
                curr_node = curr_node.edges[letter]
                new_word = curr_word + [letter]
                
                if DEBUG_GENERATE_MOVES:
                    print(indent + "building up suffix: " + str(new_word))
                self.generate_moves_for_hook_spot(curr_node, curr_rack, new_word,
                                    curr_offset + 1, hook_row, hook_col, direction, boundary,
                                    valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT)
            elif DEBUG_GENERATE_MOVES:
                print (indent + "unable to continue building suffix")
                
    def generate_moves_for_hook_spot(self, curr_node, curr_rack, curr_word, 
                       curr_offset, hook_row, hook_col, direction, boundary,
                       valid_crossword_score_dict, indent):        
        if direction == HORIZONTAL:
            (curr_row, curr_col) = (hook_row, hook_col + curr_offset)
        else:
            (curr_row, curr_col) = (hook_row + curr_offset, hook_col)
    
        if DEBUG_GENERATE_MOVES:
            print(indent + "Entering generate moves at: " + str((curr_row, curr_col)) + \
                  " with word " + str(curr_word) + " in current rack: " + str(curr_rack))
        #stop placing if we've reached the previous hook spot (or if we pass the max boundary of the board)
        if (direction == HORIZONTAL and curr_col < boundary) or \
           (direction == VERTICAL and curr_row < boundary) or \
           (curr_col >= MAX_COL) or (curr_row >= MAX_ROW):
            if DEBUG_GENERATE_MOVES:
                print (indent + GEN_MOVES_PRINT_INDENT + "reached a boundary")
            return
        
        #if there is already a tile here, try to place this as the next move
        if self.is_scrabble_tile(curr_row, curr_col):
            letter = self.board[curr_row][curr_col]
            if DEBUG_GENERATE_MOVES:
                print(indent + GEN_MOVES_PRINT_INDENT + "found an existing tile " + letter + " at " + str((curr_row, curr_col)))
            #read in the gaddag file for this letter 
            if curr_node is None:
                #curr_node = scrabble_apprentice_gaddag.read_gaddag_by_letter(letter).start_node
                curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
            self.concatenate_next(letter, curr_node, curr_rack, curr_word,
                       curr_offset, hook_row, hook_col, direction, boundary,
                       valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)

        #otheriwse, if we still have tiles left, try to place
        elif curr_rack:
            #iterate over the set of valid crossletters
            if (curr_row, curr_col) in valid_crossword_score_dict.keys():
                for letter in valid_crossword_score_dict[(curr_row, curr_col)].keys():
                    if DEBUG_GENERATE_MOVES:
                        print(indent + GEN_MOVES_PRINT_INDENT + "trying to find letter " + letter + \
                              " with word " + str(curr_word) + " in current rack: " + str(curr_rack))
                    if letter in curr_rack:
                        new_rack = curr_rack[:]
                        new_rack.remove(letter)
                        if DEBUG_GENERATE_MOVES:
                            print(indent + GEN_MOVES_PRINT_INDENT + "found letter " + letter + "--new rack is " + str(new_rack))
                        #read in the gaddag file for this letter 
                        if curr_node is None:
                            #curr_node = scrabble_apprentice_gaddag.read_gaddag_by_letter(letter).start_node
                            curr_node = SCRABBLE_APPRENTICE_GADDAG.start_node
                        self.concatenate_next(letter, curr_node, new_rack, curr_word,
                                   curr_offset, hook_row, hook_col, direction, boundary,
                                   valid_crossword_score_dict, indent + GEN_MOVES_PRINT_INDENT + GEN_MOVES_PRINT_INDENT)
        
    def generate_all_possible_moves(self, rack):
               
        for row in range(MIN_ROW, MAX_ROW):
            (valid_hook_spots, valid_crossword_score_dict) = \
                self.pull_hooks_and_crosswords(row, MIN_COL, HORIZONTAL, rack) 
                
            prev_hook_spot = MIN_COL
            for (hook_row, hook_col) in valid_hook_spots:
                if DEBUG_ALL_MOVES:
                    print("Generating moves for this hook spot: " + str((hook_row, hook_col)))
                self.generate_moves_for_hook_spot(None, rack, [], 0, hook_row, hook_col, \
                                                  HORIZONTAL, prev_hook_spot, valid_crossword_score_dict, "")
                prev_hook_spot = hook_col + 1
            if DEBUG_ALL_MOVES:
                print("\nAll possible moves to play for row: " + str(row))
                print(str(board.comp_all_possible_moves[HORIZONTAL]))
        
    
    
        for col in range(MIN_COL, MAX_COL):
            (valid_hook_spots, valid_crossword_score_dict) = \
                self.pull_hooks_and_crosswords(MIN_ROW, col, VERTICAL, rack)     
            prev_hook_spot = MIN_ROW
            for (hook_row, hook_col) in valid_hook_spots:
                if DEBUG_ALL_MOVES:
                    print("Generating moves for this hook spot: " + str((hook_row, hook_col)))
                self.generate_moves_for_hook_spot(None, rack, [], 0, hook_row, hook_col, \
                                                  VERTICAL, prev_hook_spot, valid_crossword_score_dict, "")
                prev_hook_spot = hook_row + 1
            if DEBUG_ALL_MOVES:
                print("\nAll possible moves to play for col: " + str(col))
                print(str(board.comp_all_possible_moves[VERTICAL]))
           
        
    #functions for making a move on the board
    #these return the score so that the game_play and player classes can keep a running score for each player
    def make_computer_move(self, player):
        self.clear_comp()
        self.generate_all_possible_moves(player.rack)
        #self.print_max_move()
        if self.comp_max_word:
            self.place_word(self.comp_max_row, self.comp_max_col, self.comp_max_direction, self.comp_max_word, player)
        return (self.comp_max_score, self.comp_max_word)
    
    def make_human_move(self, start_row, start_col, direction, word, player):
        print(start_row, start_col, direction, word) 
        num_tiles = len(word)
        if direction == HORIZONTAL:
            end_row = start_row + 1
            end_col = start_col + num_tiles
            cross_direction_description = "vertically"
        else:
            end_row = start_row + num_tiles
            end_col = start_col + 1
            cross_direction_description = "horizontally"
    
        #validity checks
        if self.is_valid_word(word):
            #pull these regardless of whether words have been placed, b/c we need these to calculate the score
            (valid_hook_spots, valid_crossword_score_dict) = \
                self.pull_hooks_and_crosswords(start_row, start_col, direction, player.rack)
            #exception for first move
            if self.num_words_placed == 0:
                if not self.intersect_center_tile(start_row, start_col, direction, word):
                    raise ValueError("The first move on the board must intersect the center tile")
            #all other moves
            else:
                hooks_onto_tile = False
                for curr_row in range(start_row, end_row):
                    for curr_col in range(start_col, end_col):
                        to_place = word[curr_row - start_row + curr_col - start_col] #the extra blank padding only appears when printing
                        if self.is_scrabble_tile(curr_row, curr_col):
                            if self.board[curr_row][curr_col] != to_place:
                                raise ValueError('Your tile {0} overlaps existing tiles on the board (perhaps from a concurrent session?)'.format(to_place))
                            else:
                                hooks_onto_tile = True
                        else:
                            if (curr_row, curr_col) not in valid_crossword_score_dict.keys():
                                raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(to_place, cross_direction_description))
                            elif to_place not in valid_crossword_score_dict[(curr_row, curr_col)].keys():
                                raise ValueError("Your placed tile {0} fails to form a valid crossword going {1}".format(to_place, cross_direction_description))
                            if (curr_row, curr_col) in valid_hook_spots:
                                hooks_onto_tile = True
                #check if we connected to a tile at some point in the word
                if not hooks_onto_tile:
                    raise ValueError("Your tiles must be placed adjacent to at least one tile on the board")
        else:
            raise ValueError("{0} is not a valid word in the TWL06 Scrabble dictionary".format("".join(word)))
                        
        #score and place word
        human_score = self.calc_word_score(start_row, start_col, direction, word, valid_crossword_score_dict)
        self.place_word(start_row, start_col, direction, word, player)
        return human_score
        
    def find_filled_rows_and_cols(self, placed_tiles):
        rows = set([])
        cols = set([])
        for row in range(MIN_ROW, MAX_ROW):
            for col in range(MIN_COL, MAX_COL):
                if placed_tiles[row][col] != "":
                    rows.add(row)
                    cols.add(col)
        return (rows, cols) 
        
    def convert_placed_tiles_to_full_placement(self, placed_tiles):
        (filled_rows, filled_cols) = self.find_filled_rows_and_cols(placed_tiles)
        if len(filled_rows) == 0:
            raise ValueError("You must place at least one tile! If you cannot move, exchange tiles or pass your turn")
        elif len(filled_rows) == 1:
            direction = HORIZONTAL 
        elif len(filled_cols) == 1: 
            direction = VERTICAL 
        else:
            raise ValueError("You can only place in one row or column!!!")        
        #the leftmost / uppermost point of adjacency 
        anchor_row = min(filled_rows)
        anchor_col = min(filled_cols)        
        
        #similar to the pull_valid_crossword_score function...
        prefix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, direction, 'PREFIX')
        suffix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, direction, 'SUFFIX')
        print("prefix: {0}, suffix: {1}, placed_tiles {2}, anchor_row {3}, anchor_col {4}".format(prefix, suffix, placed_tiles, anchor_row, anchor_col))
        word = prefix + [placed_tiles[anchor_row][anchor_col]] + suffix
        
        #exception for one tile placements--the official direction is the direction that creates the longer word 
        if len(word) == 1:
            flipped_direction = direction * - 1
            flipped_prefix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, flipped_direction, 'PREFIX')
            flipped_suffix = self.find_word_from_anchor(placed_tiles, anchor_row, anchor_col, flipped_direction, 'SUFFIX')
            flipped_word = flipped_prefix + [placed_tiles[anchor_row][anchor_col]] + flipped_suffix
            if len(flipped_word) > 1:
                word = flipped_word 
                direction = flipped_direction 
                prefix = flipped_prefix
                suffix = flipped_suffix
        #the actual start of the word -- since there would be existing tiles to the left / top of the anchor tile 
        if direction == HORIZONTAL:
            start_row = anchor_row 
            start_col = anchor_col - len(prefix)
        else:
            start_row = anchor_row - len(prefix)
            start_col = anchor_col 
            
        #check that there aren't extra tiles placed beyond the end of the word (since we walked down until finding an empty spot 
        if (max(filled_rows) > start_row + len(word) - 1) or (max(filled_cols) > start_col + len(word) - 1):
            raise ValueError("All of your placed tiles must be connected!") 
            
        return {"start_row": start_row, "start_col": start_col, "direction": direction, "word": word}
        
    #given the starting placement--i.e. the anchor tile--determine the prefix and suffix (since the full word may include tiles on the board) 
    def find_word_from_anchor(self, placed_tiles, anchor_row, anchor_col, direction, prefix_or_suffix):
        if direction == HORIZONTAL:
            (row_delta, col_delta) = (0, 1)
        else:
            (row_delta, col_delta) = (1, 0)
        if prefix_or_suffix == 'PREFIX':
            (row_delta, col_delta) = (row_delta * -1, col_delta * -1)
            
        word_fix = []
        (curr_row, curr_col) = (anchor_row, anchor_col)
        print("Find start for {0} at {1} {2}".format(word_fix, curr_row, curr_col))
        while True:
            (curr_row, curr_col) = (curr_row + row_delta, curr_col + col_delta)
            if curr_row >= MIN_ROW and curr_row < MAX_ROW and curr_col >= MIN_COL and curr_col < MAX_COL:
                if self.is_scrabble_tile(curr_row, curr_col):
                    letter = self.board[curr_row][curr_col]
                else:
                    letter = placed_tiles[curr_row][curr_col]
                print(curr_row, curr_col, letter) 
                if letter != "":
                    word_fix.append(letter) #insert in front
                else:
                    break
            else:
                break
        print(word_fix) 
        if prefix_or_suffix == 'PREFIX':
            return word_fix[::-1]
        return word_fix 

        
#instantiates a player bound to a particular board and common scrabble bag
IS_HUMAN = True
IS_COMPUTER = False
PRINT_DIVIDER = "----------------------------"
class scrabble_player:
    def __init__(self, name, is_human, board):
        self.name = name
        self.is_human = is_human
        self.rack = []  
        self.running_score = 0
        self.words_played = []
        
    def print_player_state(self):
        print(PRINT_DIVIDER)
        print("Current running score for " + self.name + ": " + str(self.running_score) + " pts")
        print("Current rack for " + self.name + ": " + ''.join(self.rack))
        print("Words played and scores:")
        for (pos, (word, score)) in enumerate(self.words_played):
            print(str(pos + 1) + ". " + ''.join(word) + " - " + str(score) + " pts")
            
#master class that holds all of the boards and players
#provides all of the front end functions for interfacing with the web page/application
MAX_NUM_ATTEMPTED_MOVES = 5 

class game_play:
    def __init__(self, board, 
                 scrabble_player_1, 
                 scrabble_player_2 = None,
                 scrabble_player_3 = None,
                 scrabble_player_4 = None):
        self.board = board
        self.current_player = scrabble_player_1
        self.round_num = 1 
        self.num_turns_passed = 0
        self.play_order = []
        #set the play order, and draw tiles for each player
        for player in [scrabble_player_1, scrabble_player_2, scrabble_player_3, scrabble_player_4]:
            if player:
                self.play_order.append(player)
                self.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES)
       
    def print_game_state(self):
        print(PRINT_DIVIDER)
        print("Current Round: " + str(self.round_num))
        print("Play Order: WILL BE FINISHED")
        #+ ", ".join(self.play_order))
        print("Number of tiles left in the bag: " + str(len(scrabble_bag)))
        self.board.print_board()
        print("Current player: " + self.current_player.name)

    
    def draw_tiles_end_of_turn(self, player, num_tiles):
        self.draw_from_scrabble_bag(player, num_tiles)
        
    #exchange up to the # of tiles remaining in the bag (the first n tiles in tiles_to_exchange are used)
    def exchange_tiles_during_turn_capped(self, player, tiles_to_exchange):
        tiles_left_in_bag = len(self.board.bag)
        print(tiles_left_in_bag)
        print("exchange_tiles_during_turn_capped: tiles_to_exchange {0}, tiles_left_in_bag {1}".format(tiles_to_exchange, tiles_left_in_bag))
        if tiles_left_in_bag == 0:
            raise ValueError("Nothing can be exchanged because no tiles are left in the bag")
        if len(tiles_to_exchange) > tiles_left_in_bag:
            print("truncating") 
            self.exchange_tiles_during_turn(player, tiles_to_exchange[0:tiles_left_in_bag])
        else:
            print("regular")
            self.exchange_tiles_during_turn(player, tiles_to_exchange)
            
    def exchange_tiles_during_turn(self, player, tiles_to_exchange):
        if len(tiles_to_exchange) == 0:
            raise ValueError("You must exchange at least 1 tile")
        self.draw_from_scrabble_bag(player, len(tiles_to_exchange), tiles_to_exchange)
             
    def draw_from_scrabble_bag(self, player, num_tiles_to_draw, tiles_to_exchange = None):
        if tiles_to_exchange and num_tiles_to_draw != len(tiles_to_exchange):
            raise ValueError("Don't cheat. You're trying to draw more tiles than you are exchanging")
        
        print("num_tiles_to_draw: {0}, tiles_to_exchange: {1}".format(num_tiles_to_draw, str(tiles_to_exchange)))
        if num_tiles_to_draw < 1 or num_tiles_to_draw > RACK_MAX_NUM_TILES:
            raise ValueError("You must {0} between 1 and {1} tiles".format("exchange" if tiles_to_exchange else "draw", RACK_MAX_NUM_TILES))
        
        num_tiles_left = len(self.board.bag) 
        if num_tiles_to_draw > num_tiles_left and tiles_to_exchange:
            raise ValueError("Not enough tiles left--you can only exchange up to {0} tiles".format(num_tiles_left))
        num_tiles_to_draw = min(num_tiles_to_draw, num_tiles_left) 
        
        #not true in game end conditions 
        #ending_tiles = len(player.rack) if tiles_to_exchange else num_tiles_to_draw + len(player.rack)
        #if ending_tiles != RACK_MAX_NUM_TILES:
        #    raise ValueError("When {0} tiles, you must end up with exactly {1} tiles in your rack".format("exchanging" if tiles_to_exchange else "drawing", RACK_MAX_NUM_TILES)) 
             
        #if exchanging tiles, first remove these from rack and append back to the bag 
        if tiles_to_exchange:
            #create a copy first to validate that all requested tiles can actually be exchanged
            new_rack = player.rack[:]
            new_bag = self.board.bag[:]
            for tile in tiles_to_exchange:
                try:
                    new_rack.remove(tile)
                    new_bag.append(tile)
                    print(tile + " added back to bag")
                except:
                    print("Attempted to exchange tiles that are not in your rack. Don't cheat!")
                    return
            player.rack = new_rack[:]
            self.board.bag = new_bag[:]
            random.shuffle(self.board.bag)
        
        #now draw to fill back up the player's rack    
        for i in range(0, num_tiles_to_draw):
            letter = random.choice(self.board.bag)
            self.board.bag.remove(letter)
            player.rack.append(letter)
            print("Drew tile {0}".format(letter))
        
    def request_human_move(self, player):
        input_exchange = input("Would you like to exchange tiles? Type 'Yes' to exchange (otherwise, you will make your move)")
        if input_exchange.upper() == "YES":
            tiles_to_exchange_raw = input("Enter the tiles you would like to exchange: ")
            tiles_to_exchange = list(tiles_to_exchange_raw)
            self.exchange_tiles_during_turn(player, tiles_to_exchange)
            return (None, None, None, None)
        else:
            input_word_raw = input("Enter the full word you would like to place: ")
            input_word = list(input_word_raw.upper())
            
            input_row_raw = int(input("Enter the starting row: "))
            while (input_row_raw < MIN_ROW or input_row_raw >= MAX_ROW):
                input_row_raw = int(input("Please enter a valid starting row: "))
            input_row = input_row_raw
            
            input_col_raw = int(input("Enter the starting column: "))
            while (input_col_raw < MIN_COL or input_col_raw >= MAX_COL):
                input_col_raw = int(input("Please enter a valid starting column: "))
            input_col = input_col_raw

            input_dir_raw = input("Enter the direction (horizontal/vertical): ")
            while (input_dir_raw.upper() != "HORIZONTAL" and input_dir_raw != "VERTICAL"):
                input_dir_raw = input("Please enter a valid direction: ") 
            if input_dir_raw.upper() == "HORIZONTAL":
                input_dir = HORIZONTAL
            else:
                input_dir = VERTICAL

            return (input_row, input_col, input_dir, input_word)
        
    def play_move(self, player):
        self.print_game_state()
        player.print_player_state()
        
        if player.is_human:
            num_attempts = 0
            while True:
                (input_row, input_col, input_dir, input_word) = self.request_human_move(player)
                if input_word:
                    try:
                        score = self.board.make_human_move(input_row, input_col, input_dir, input_word, player)
                        break
                    except:
                        print("Made Illegal Move. Let's try again.")
                        num_attempts += 1
                        if num_attempts == MAX_NUM_ATTEMPTED_MOVES:
                            print("You fail at entering moves on a Scrabble board. Your turn will be skipped.")
                            break
                else:
                    player.print_player_state()
                    return
        else:
            print("Computer thinking through move....")
            (score, input_word) = self.board.make_computer_move(player)
            #if the computer is unable to find a move, exchange tiles
            if not input_word:
                self.exchange_tiles_during_turn(player, player.rack)
                

        player.words_played.append((input_word, score))
        player.running_score += score   
        self.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES - len(player.rack)) 
        player.print_player_state()
        
    def play_game(self):
        print("Beginning game!")
        while True:
            for player in self.play_order:
                self.play_move(player)
            self.round_num += 1
            if self.game_has_ended():
                break
                
    def game_has_ended(self):
        return self.game_end_reason() != ""
    
    #game ends if (1) six turns have ended in passes or (2) a player has no tiles left and there are no tiles left in the bag 
    def game_end_reason(self):
        if self.num_turns_passed == MAX_TURNS_PASSED: 
            return "Game over: {0} turns have ended in passes".format(MAX_TURNS_PASSED)
        if len(self.board.bag) == 0:
            for player in self.play_order: 
                if len(player.rack) == 0: 
                    return "Game over: {0} used up all tiles in rack, and no tiles are left in the bag".format(player.name)
        return ""
    
    def print_end_state(self):
        print("Game has ended!")
        print("Final results:")
        self.print_game_state()
        for player in self.play_order:
            player.print_player_state()
          
if __name__ == "__main__":
    scrabble_corpus = load_scrabble_corpus()
    scrabble_apprentice_gaddag.write_gaddag_full(scrabble_corpus)

    
    
