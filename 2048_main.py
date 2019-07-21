# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:22:01 2018

@author: Andy
"""
import numpy as np
import random
import csv
import matplotlib.pyplot as plt

class Game:
    gamestate = np.array([(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)])
    def init():
        """initializes the board back to empty"""
        Game.gamestate=np.array([(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)])
        
    def state():
        """returns the current gamestate"""
        currentstate=np.copy(Game.gamestate)                                    #give back a copy of the gamestate
        return currentstate
    
    def empty_spaces(matrix):
        """list position-tuples of all empty spaces on matrix-board"""
        empty_entries = []
        for i in range(0,4):                                                    #check all tiles
            for j in range(0,4):
                if matrix[i,j] == 0:
                    empty_entries.append((i,j))                                 #if empty (=0), add their coordinates to the list
        return empty_entries
		
    def rotate_entriesCW(matrix):
        """rotate a matrix clockwise"""
        use_matrix=np.copy(matrix)
        swap_matrix=np.array([(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0)])
        newmatrix=use_matrix.transpose()                                        #the composition of transposition and multiplying with a mirrored matrix "turns" the matrix
        newmatrix=np.matmul(newmatrix,swap_matrix)
        return newmatrix
		
    def rotate_entriesACW(matrix):
        """rotate a matrix anti-clockwise"""
        use_matrix=np.copy(matrix)
        swap_matrix=np.array([(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0)])
        newmatrix=np.matmul(use_matrix,swap_matrix)
        newmatrix=newmatrix.transpose()
        return newmatrix
	
    def is_over(matrix):
        """checks if legal move on the board"""
        returnvalue = True
        if not len(Game.empty_spaces(matrix)) == 0:                              #if there are empty tiles on the board there must be a legal move
            returnvalue= False
        else:
            i=0
            while i in range(0,4) and returnvalue==True:
                j=0
                while j in range(0,3) and returnvalue==True:
                    if matrix[i,j]== matrix[i,j+1]:                             #check vertically if there are adjacent cells with the same value that could be combined which would imply a legal move
                        returnvalue= False
                    j+=1
                i+=1
            i=0
            while i in range(0,3) and returnvalue == True:
                j=0
                while j in range(0,4) and returnvalue == True:
                    if matrix[i,j]== matrix[i+1,j]:                              #same check horizontally
                        returnvalue= False
                    j+=1
                i+=1
        return returnvalue
        
    def checkmoveUP(matrix):
        """checks if the given boardstate is compatible with the move UP/N"""
        legality = False
        j=0
        while j in range(0,4) and legality==False:
            i=0
            while i in range(0,3) and legality==False:
                if matrix[i,j] == 0 and not matrix[i+1,j]  == 0:                #checks if there is an empty tile directly above a nonempty one, if so the move up must be legal
                    legality = True
                i+=1
            j+=1
        j=0
        while j in range(0,4) and legality == False:
            i=0
            while i in range(0,3) and legality == False:
                if matrix[i,j] == matrix[i+1,j] and not matrix[i,j] == 0:       #checks if there are two identical (nonempty) tiles directly above eachother, is so a move combining them must be legal
                    legality = True
                i+=1
            j+=1
        return legality
	
    def checkmove(matrix,direction):
        """checks if a boardstate is compatible with a move in the given direction"""
        test_matrix = np.copy(matrix)
        movelegality = False
        if direction == "W":                                                    #this applies checkmoveUp by just rotating the matrix into an orientation where our move becomes N/UP
            movelegality=Game.checkmoveUP(test_matrix)
        if direction == "D":
            test_matrix = Game.rotate_entriesACW(test_matrix)
            movelegality=Game.checkmoveUP(test_matrix)
        if direction == "A":
            test_matrix = Game.rotate_entriesCW(test_matrix)
            movelegality=Game.checkmoveUP(test_matrix)
        if direction == "S":
            test_matrix = Game.rotate_entriesCW(test_matrix)
            test_matrix = Game.rotate_entriesCW(test_matrix)
            movelegality=Game.checkmoveUP(test_matrix)
        return movelegality
    
    def current_score(matrix):                                                  #simply returns the total value of a board by adding all tile values.
        """returns the score of a matrix-board"""
        score=0
        for i in range(0,4):
            for j in range(0,4):
                score+=matrix[i,j]
        return score
    
    def highest_tile(matrix):
        """ returns the highest tile of a matrix board"""
        tile_num = 0
        for i in range(0,4):
            for j in range(0,4):
                if matrix[i,j] > tile_num:
                    tile_num = matrix[i,j]
        return tile_num
    
    def average_value(matrix):                                                  #this is a more advanced score version where we divide the score by the number of nonempty tiles
        """returns the average tilevalue of a board 
        (this excludes empty tiles)"""
        emptylist=Game.empty_spaces(matrix)
        totalvalue=Game.current_score(matrix)
        averagevalue=totalvalue/(16-len(emptylist))
        return averagevalue
	
    def moveUP(matrix):
        """executes the move UP/N on a boardstate"""
        newmatrix=np.copy(matrix)
        move_matrix=np.copy(matrix)
        for j in range(0,4):                                                    #consolidates the tiles at the top edge
            nonzero_tiles=[]
            for i in range(0,4):
                if not move_matrix[i,j] == 0:
                    nonzero_tiles.append(move_matrix[i,j])
            for k in range(0,4):
                if k < len(nonzero_tiles):
                    newmatrix[k,j]=nonzero_tiles[k]
                else:
                    newmatrix[k,j]=0
        final_matrix = np.copy(newmatrix)
        for j in range(0,4):                                                    #merges duplicate neighbors into superior tiles and ensure the board gets adjusted
            if newmatrix[0,j]==newmatrix[1,j]:                                  #checks if the first and second entry are identical
                final_matrix[0,j]= newmatrix[0,j]+newmatrix[1,j]
                if newmatrix[2,j]==newmatrix[3,j]:                              #this is the case where 1st=2nd and 3rd=4th so we have the combined tiles in the 1st and 2nd entry and then fill with 0s
                    final_matrix[1,j]=newmatrix[2,j]+newmatrix[3,j]
                    final_matrix[2,j]=0
                    final_matrix[3,j]=0
                else:                                                           #in this case only 1st=2nd so we merge and then move up the other 2 tiles and add a 0
                    final_matrix[1,j]=newmatrix[2,j]
                    final_matrix[2,j]=newmatrix[3,j]
                    final_matrix[3,j]=0
            elif newmatrix[1,j]==newmatrix[2,j]:                                #this case is only 2nd=3rd so 1st entry stays unchanged 
                final_matrix[1,j]=newmatrix[1,j]+newmatrix[2,j]
                final_matrix[2,j]=newmatrix[3,j]
                final_matrix[3,j]=0
            elif newmatrix[2,j]==newmatrix[3,j]:                                #last "special case" where 3rd=4th so they merge and we empty the last cell.
                final_matrix[2,j]=newmatrix[2,j]+newmatrix[3,j]
                final_matrix[3,j]=0
        return final_matrix
    
    def move(matrix,direction):                                                 #applies moveUP by rotating the matrix into the needed position and then afterwards rotates them back
        """checks if a move is legal on a boardstate and executes it if legal
        if move legal returns the new boardstate and True
        if move illegal returns the original boardstate and False"""
        legality=False
        move_matrix=np.copy(matrix)
        return_matrix=np.copy(matrix)
        manipulated_matrix = np.copy(matrix)
        legality= Game.checkmove(move_matrix,direction)
        if direction== "W" and legality == True:
            return_matrix = Game.moveUP(move_matrix)
        if direction== "D" and legality == True:
            manipulated_matrix = Game.rotate_entriesACW(move_matrix)
            manipulated_matrix = Game.moveUP(manipulated_matrix)
            return_matrix = Game.rotate_entriesCW(manipulated_matrix)
        if direction== "A" and legality == True:
            manipulated_matrix = Game.rotate_entriesCW(move_matrix)
            manipulated_matrix = Game.moveUP(manipulated_matrix)
            return_matrix = Game.rotate_entriesACW(manipulated_matrix)
        if direction == "S" and legality == True:
            manipulated_matrix = Game.rotate_entriesACW(move_matrix)
            manipulated_matrix = Game.rotate_entriesACW(manipulated_matrix)
            manipulated_matrix = Game.moveUP(manipulated_matrix)
            manipulated_matrix = Game.rotate_entriesACW(manipulated_matrix)
            return_matrix = Game.rotate_entriesACW(manipulated_matrix)
        return (return_matrix,legality)
    
    def future_av_value(matrix,direction):                                      #hypothetically executes a move and gives back the average (nonempty) tilevalue after that move
        """predict the average tilevalue after a given move on the current board
        this does not take into account the random tilespawn
        returns 0 if move illegal"""
        legality=False
        future_matrix=np.copy(matrix)
        predict_matrix=np.copy(matrix)
        future_value=0
        future_matrix,legality= Game.move(predict_matrix,direction)
        if legality == True:
            future_value=Game.average_value(future_matrix)
            return future_value
        else:
            return 0
    
    def tile_spawn(matrix):                                                     #this first picks a random empty tile using the empty_spaces and then inserts a 2 or 4 into that position 
        """spawns a 2 or a 4 on the board in an empty spot
        90% chance for 2
        10% for 4"""
        spawned_matrix = np.copy(matrix)
        empty_spaces = Game.empty_spaces(spawned_matrix)
        empty_count = len(empty_spaces)
        spawnposition=random.randint(1,empty_count) -1
        a,b=empty_spaces[spawnposition]
        two_or_four=random.randint(1,10)
        if two_or_four== 1:
            spawned_matrix[a,b]=4
        else:
            spawned_matrix[a,b]=2
        return spawned_matrix

                           
class Human_Player:
    
    def __init__(self, name):
        self.counter = 0
        self.name = name
    
    def move(self, board): #condition: game must not be over
        movelegality = False
        direction = None
        while not movelegality :
            direction = str(input("Please Enter a valid Direction from W,A,S,D: ")).upper()
            movelegality = Game.checkmove(board,direction)
            if direction == "EXIT":
                movelegality = 1
        if direction == "EXIT":
            return direction
        else:
            board = Game.move(board,direction)
            self.counter+=1
            return board[0]

    def __str__(self):
        return self.name        
    
# Test for Human_Player        
#player_Human = Human_Player("name")
#spielstand = Game.gamestate
#for i in range(500):
 #   spielstand = Game.tile_spawn(spielstand)
  #  if Game.is_over(spielstand):
   #     break
    #spielstand = player_Human.move(spielstand)
    #print(spielstand)  
#print(spielstand) 
 

class Left_Down:#Left then down, else right or up
    def __init__(self):
        self.counter = 0
    def __str__(self):
        return "W-S-E-N"
    
    def move(self,board):#condition: game must not be over
        
        if Game.checkmove(board,"A"):
            board = Game.move(board,"A")
        elif Game.checkmove(board,"S"):
            board = Game.move(board,"S")
        elif Game.checkmove(board,"D"):
            board = Game.move(board,"D")
        elif Game.checkmove(board,"W"):
            board = Game.move(board,"W")
        else:
            print("there is an error")
    
        self.counter +=1
        return board[0]
    
    
"""
# Test for Left_Down_Player
player_ld = Left_Down()
spielstand = Game.gamestate
for i in range(500):
    spielstand = Game.tile_spawn(spielstand)
    if Game.is_over(spielstand):
        break
    spielstand = player_ld.move(spielstand)
    print(spielstand)  
print("final gamestate: \n",spielstand, "\n Nr. of Moves: ", player_ld.counter) 
"""

class Random:
    def __init__(self):
        self.counter = 0
    def __str__(self):
        return "Random"
    
    def move(self, board):
        direction = random.choice(["W","D","S","A"])
        while not Game.checkmove(board, direction):
            direction = random.choice(["W","D","S","A"])
        board = Game.move(board, direction)
        self.counter += 1
        return board[0]
"""
# Test for Random_Player
player_rand = Random()
spielstand = Game.gamestate
for i in range(500):
    spielstand = Game.tile_spawn(spielstand)
    if Game.is_over(spielstand):
        break
    spielstand = player_rand.move(spielstand)
    print(spielstand)  
print("final gamestate: \n",spielstand, "\n Nr. of Moves: ", player_rand.counter)
"""			
class Simple_Max:
    def __init__(self):
        self.counter = 0
    def __str__(self):
        return "Simple Max"
    
    def move(self, board):
        test_board = np.copy(board)
        max_average_value = 0
        for direction in ["A","D","S","W"]:
            if Game.future_av_value(test_board, direction) >= max_average_value and Game.checkmove(test_board,direction):
                board = Game.move(test_board,direction)
        self.counter += 1
        return board[0]
"""
# Test for Simple_max_Player
player_simple_max = Simple_Max()
spielstand = Game.gamestate
for i in range(500):
    spielstand = Game.tile_spawn(spielstand)
    if Game.is_over(spielstand):
        break
    
    spielstand = player_simple_max.move(spielstand)
    print(spielstand)  
print("final gamestate: \n",spielstand, "\n Nr. of Moves: ", player_simple_max.counter)		
"""

class Prob_Max:
    def __init__(self):
        self.counter = 0
        
    def __str__(self):
        return "Prob Max"
    
    def move(self,board):
        
        max_sum_of_max_av_value = 0
        best_direction = "A"
        for first_direction in ["A","D","S","W"]: # go through all directions 
            sum_of_max_av_values = 0
            first_test_board = np.copy(board)
            if Game.checkmove(first_test_board,first_direction):
                first_test_board = Game.move(first_test_board,first_direction)
                first_test_board = Game.tile_spawn(first_test_board[0]) 
                
                for seccond_direction in ["A","D","S","W"]: # sum the possible values from all directions for the seccond time 
                    sum_of_max_av_values += Game.future_av_value(first_test_board, seccond_direction)
                if sum_of_max_av_values >= max_sum_of_max_av_value:
                    max_sum_of_max_av_value = sum_of_max_av_values
                    best_direction = first_direction # and choose the first direction with the highest sum
        board = Game.move(board,best_direction)
        self.counter += 1
        return board[0]
        
      
""" 
# Test for Prob_Max
player_prob_max = Prob_Max()
spielstand = Game.gamestate
for i in range(1000):
    spielstand = Game.tile_spawn(spielstand)
    if Game.is_over(spielstand):
        break
    spielstand = player_prob_max.move(spielstand)
     
print("final gamestate: \n",spielstand, "\n Nr. of Moves: ", player_prob_max.counter,"\n final av. Value: ", Game.average_value(spielstand) )	   
"""
#########GUI classes

class Shell_UI:
    def __init__(self, board, score = 0, auto_display = True):
        '''Create appropiate board string without values (assume max. number length of 6 digits)'''
        num_len=7
        num_place = '{:^'+str(num_len)+'}'
        upL, upM,upR= u'\u250F',u'\u2533',u'\u2513'
        hor, ver, emp =u'\u2501',u'\u2503',u'\u0000'
        leM, miM, riM=u'\u2523', u'\u254B', u'\u252B'
        loL,loM,loR=u'\u2517', u'\u253B', u'\u251B'
        self.score =""
        self.board = board
        self.rows = len(board)
        self.col = len(board[0])  
        self.up_row= upL+hor*num_len+(upM+hor*num_len)*(self.col-1)+upR+'\n'
        self.emp_row= (ver+num_len*emp)*self.col+ver+'\n'
        self.num_row= self.emp_row+(ver+num_place)*self.col+ver+'\n'+self.emp_row
        self.mid_row=leM+hor*num_len+(miM+hor*num_len)*(self.col-1)+riM+'\n'
        self.low_row=loL+hor*num_len+(loM+hor*num_len)*(self.col-1)+loR+'\n'
        self.board_s=self.up_row+self.num_row+(self.mid_row+self.num_row)*(self.rows-1)+self.low_row
        self.score_display = '{:^'+str((num_len+1)*self.col-1)+'}'
        if score:
            self.format_score(score)
        if auto_display:
            self.display()
    
    def format_score(self, num):
        self.score_str="Score: {}".format(num)
        self.score = self.score_display.format(self.score_str)
   
    def display(self):
        '''Take current board values as strings, format them into the empty board and print.'''
        self.l_places = []
        for row in range(len(self.board)):
            for place in self.board[row]:
                if place:
                    self.l_places.append(str(place))
                else:
                    self.l_places.append('')
        print(self.board_s.format(*self.l_places)+ self.score)
        
    def update(self,new_board, new_score = False, auto_display = True):
        '''Update board values with new list of lists in the same size as the previous one'''
        self.board = new_board
        if new_score:
            self.format_score(new_score)
        if auto_display:
            self.display()
    

class Pretty_UI:
    def __init__(self, board, score = 0):
        '''Create Figure and axes and update it with the givenboard and score'''
        self.emp_farb = 'xkcd:Eggshell'
        self.bg_farb = 'xkcd:greyish blue'
        self.farb_dic = {
            '': [self.emp_farb, 'Black'],
            '2':["xkcd:Light Blue",'Blue'],
            '4':["xkcd:Sky Blue",'Blue'],
            '8':["xkcd:Aqua",'Green'],
            '16':["xkcd:Pistachio", 'Brown'],
            '32':["xkcd:Grass",'White'], 
            '64':["xkcd:Puke Green",'White'],
            '128':["xkcd:Mustard Yellow",'White'],
            '256':["xkcd:GoldenRod",'White'],
            '512':["xkcd:Melon",'White'],
            '1024':["xkcd:Faded Pink",'White'],
            '2048':["xkcd:BubbleGum Pink",'White'],
            '4096':["xkcd:Lilac",'White'],
            '8192':["xkcd:Periwinkle",'White']
            }
        
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.text_list = []            
        self.fig, self.axes = plt.subplots(self.rows,self.cols, facecolor = self.bg_farb, constrained_layout = True) 
        #self.fig.set_constrained_layout_pads(top=0.7,bottom=0.11, left=0.17, right=0.855,hspace=0.2,wspace=0.2)
        self.fig.set_size_inches(self.cols+1, self.rows+1)
        self.head=self.fig.suptitle('', fontsize=30, color= 'White')
        for i in range(self.rows):
            for j in range(self.cols):
                self.a = self.axes[i,j]
                self.a.xaxis.set_visible(False)
                self.a.yaxis.set_visible(False)
                #self.a.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
                self.text_list.append(self.a.text(0.5,0.5,'', horizontalalignment='center', verticalalignment='center', fontsize =18))
                self.a.set_fc(self.emp_farb)
        #plt.ion()
        plt.show()
        self.update(board,score)
          
    def update(self, new_board, new_score):
        '''Update axes with new board and score.'''
        self.board = new_board
        self.score=new_score
        self.l_places = []
        for row in range(self.rows):
            for place in self.board[row]:
                if place:
                    self.l_places.append(str(place))
                else:
                    self.l_places.append('') 
        k=0
        for i in range(self.rows):
            for j in range(self.cols):
                self.a = self.axes[i,j]
                self.num = self.l_places[k]
                                
                self.a.set_fc(self.farb_dic[self.num][0])
                self.text_list[k].set_text(self.num)
                self.text_list[k].set_color(self.farb_dic[self.num][1])
                k+=1
        
        self.score_label = '''Score: {}'''.format(self.score)
        self.head.set_text(self.score_label)

        self.fig.canvas.draw()
        plt.pause(0.1)
    
#################### Test for GUI #################
#gamestate_1 = np.array([(8192,4096,2048,1024),(64,128,256,512,),(32,16,8,4),(0,2,2,2)])
#gamestate_2 = np.array([(8192,4096,2048,1024),(64,128,256,512,),(32,16,8,4),(0,0,2,4)])
#score_1, score_2 = 11235813, 23571113
#
#b = Pretty_UI(gamestate_1)
#b = Pretty_UI(gamestate_1, score1)
#b.update(gamestate_2, score_2)
#
#c = Shell_UI(gamestate_1, score_1)
#c.update(gamestate_2, score_2)



# Main program to execute the game
#Choose if you want to play by yourself or let the computer play the game
player_modes=["VISUAL", "SHELL","STATISTICAL"]
player_mode=None
while player_mode not in player_modes:
    player_mode=input('- To play the game by yourself enter: "visual" \n\
- To play the game by yourself using just the shell enter: "shell" \n\
- To run a computer simulation enter: "statistical" \n\
- To exit the program enter: "Exit"  ').upper()
    # Quits program if user enters exit
    if player_mode == "EXIT":
            print("You have left the game")
            break
        
# Execute the mode where a human player plays the game
player= None
if player_mode =="SHELL":
    player = Human_Player("name")
    spielstand = Game.gamestate
    spielstand= Game.tile_spawn(spielstand)
    spielstand= Game.tile_spawn(spielstand)
    gui = Shell_UI(spielstand)
    while not Game.is_over(spielstand):
        print("Current score: ", Game.current_score(spielstand), "\nNumber of moves ", player.counter, "\nHighest tile number: ", Game.highest_tile(spielstand))
        test_spielstand = player.move(spielstand)
        if test_spielstand == "EXIT":
            break
        spielstand = np.copy(test_spielstand)
        spielstand = Game.tile_spawn(spielstand)
        gui.update(spielstand)
    print("Game is over! \nYour score is: ", Game.current_score(spielstand), "\nNumber of moves ", player.counter, "\nHighest tile number: ", Game.highest_tile(spielstand))

elif player_mode =="VISUAL":
    player = Human_Player("name")
    spielstand = Game.gamestate
    spielstand= Game.tile_spawn(spielstand)
    spielstand= Game.tile_spawn(spielstand)
    gui = Pretty_UI(spielstand)
    while not Game.is_over(spielstand):
        print("\nNumber of moves ", player.counter, "\nHighest tile number: ", Game.highest_tile(spielstand))
        test_spielstand = player.move(spielstand)
        if test_spielstand == "EXIT":
            break
        spielstand = np.copy(test_spielstand)
        spielstand = Game.tile_spawn(spielstand)
        gui.update(spielstand, Game.current_score(spielstand))
    print("Game is over! \nYour score is: ", Game.current_score(spielstand), "\nNumber of moves ", player.counter, "\nHighest tile number: ", Game.highest_tile(spielstand))

# Execute statistical mode
else:   
    Left_Down=Left_Down()
    Random= Random()
    Simple_Max = Simple_Max()
    Prob_Max = Prob_Max()
    players=[Left_Down, Random, Prob_Max, Simple_Max]
    print("Please wait for the data to be loaded...")
    with open('statistical.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Player ','Score', 'Number of moves ','Highest tile ','Game over '])    
        for player in players: # iterate over different computer strategies
            for k in range(50): # execute game k times per strategy
                spielstand = Game.gamestate
                player.counter = 0
                for i in range(1000):
                   spielstand = Game.tile_spawn(spielstand)
                   if Game.is_over(spielstand):
                       break
                   spielstand = player.move(spielstand)
                   if Game.is_over(spielstand):
                       break
                thewriter.writerow([player, Game.current_score(spielstand), player.counter, Game.highest_tile(spielstand), Game.is_over(spielstand)])
        print('Computer simulation finished. Filename: statistical.csv ' )
                    
