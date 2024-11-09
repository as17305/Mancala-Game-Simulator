# Mancala Project Code

class Pit:
        
    def __init__(self, label, seeds=4):
        self.__seeds = seeds
        self.label = label
    def is_bank(self):
        if "bank" in self.label.lower(): 
          return True
        return False
    def add_seed(self):
        self.__seeds+=1
    def set_seeds_to_zero(self):
        self.__seeds = 0 
    def get_seeds(self):
        return self.__seeds
    
class Board:
    def __init__(self,seeds=[4,4,4,4,4,4,0,4,4,4,4,4,4,0]):
        self.board = [] 
        self.player = "A"
        for i in range(14):
            if i < 6:
                self.board.append(Pit(f"A{i+1}",seeds[i]))
            elif i == 6:
                self.board.append(Pit("A BANK", seeds[i]))
            elif i < 13:
                self.board.append(Pit(f"B{i-6}",seeds[i]))
            elif i == 13:
                self.board.append(Pit("B BANK", seeds[i]))
    
    def __str__(self):
        display = []
        #put in the top row from left to right
        for i in range(12, 6, -1):
            display.append(self.board[i].label)
        for i in range(12, 6, -1):
            display.append(self.board[i].get_seeds())
        display.append(self.board[13].get_seeds())
        display.append(self.board[6].get_seeds())
        for i in range(0, 6, 1):
            display.append(self.board[i].label)
        for i in range(0, 6, 1):
            display.append(self.board[i].get_seeds())
        s = """    
+------+------+--<<<<<-Player B----+------+------+------+
B      |{}    |{}    |{}    |{}    |{}    |{}    |      A
       |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |
B      |      |      |      |      |      |      |      B
A {:2d}   +------+------+------+------+------+------+  {:2d}  A
N      |{}    |{}    |{}    |{}    |{}    |{}    |      N
K      |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |  {:2d}  |      K
       |      |      |      |      |      |      |       
+------+------+------+-Player A->>>>>-----+------+------+
        """.format(*display)
        return s
    
    def play_move(self,label):
      for i in range(len(self.board)):
        if self.board[i].label == label:
          x = self.board[i].get_seeds()
          j = 1
          while j < x + 1:
            idx = (i + j)%14
            if self.board[idx].is_bank():
              if self.player == "A":
                if (idx) == 13:
                  j += 1
                  x += 1
              else:
                if (idx) == 6:
                  j += 1
                  x += 1
              idx = (i + j)%14
            self.board[idx].add_seed()
            par = 12 - idx
            if j == x and self.board[idx].get_seeds() == 1 and self.board[par].get_seeds() > 0 and not(self.board[idx].is_bank()):
              if self.player == "A" and idx >= 0 and idx <= 5:
                self.board[idx].set_seeds_to_zero()
                z = self.board[par].get_seeds()
                self.board[par].set_seeds_to_zero()
                for k in range(z + 1):
                  self.board[6].add_seed()
              if self.player == "B" and idx >= 7 and idx <= 12:
                self.board[idx].set_seeds_to_zero()
                z = self.board[par].get_seeds()
                self.board[par].set_seeds_to_zero()
                for k in range(z + 1):
                  self.board[13].add_seed()
            if j == x and idx == 6 and self.player == "A":
              self.switch_player()
            elif j == x and idx == 13 and self.player == "B":
              self.switch_player()
            j += 1
          self.board[i].set_seeds_to_zero()

    def switch_player(self):
      if self.player == "A":
        self.player = "B"
      else:
        self.player = "A"   

    def get_valid_moves(self):
      listValid = []
      if self.player == "A":
        for i in range(6):
          if self.board[i].get_seeds() > 0:
            listValid.append(self.board[i].label)
      else:
        for i in range(7, 13):
          if self.board[i].get_seeds() > 0:
            listValid.append(self.board[i].label)
      return listValid
      
    def game_over(self):
      if len(self.get_valid_moves()) == 0:
        return True
      self.switch_player()
      if len(self.get_valid_moves()) == 0:
        return True
      self.switch_player()
      return False
      
    def results(self):
      leftover = 0 
      for i in range(0, 14):
        if i < 6:
          leftover += self.board[i].get_seeds()
          self.board[i].set_seeds_to_zero()
        elif i == 6:
          while leftover > 0:
            self.board[6].add_seed()
            leftover -= 1
          leftover = 0
        elif i > 6 and i < 13:
          leftover += self.board[i].get_seeds()
          self.board[i].set_seeds_to_zero()
        else:         
          while leftover > 0:
            self.board[13].add_seed()
            leftover -= 1
      statement = str(self)
      if self.board[6].get_seeds() == self.board[13].get_seeds():
        statement += f"Its a tie! The score was {self.board[6].get_seeds()} to {self.board[13].get_seeds()}" 
      elif self.board[6].get_seeds() > self.board[13].get_seeds():
        statement += f"Player A Wins! The score was {self.board[6].get_seeds()} to {self.board[13].get_seeds()}"  
      else:
        statement += f"Player B Wins! The score was {self.board[13].get_seeds()} to {self.board[6].get_seeds()}"  
      return statement

    def computerPlayer(self):
      import random
      valid = random.randint(0, len(self.get_valid_moves()) - 1)
      print(f"Player B's move: {self.get_valid_moves()[valid]}")
      self.play_move(self.get_valid_moves()[valid])

    def game_value(self, testMove):
      value = 0
      for a in range(len(self.board)):
        if self.board[a].label == testMove:
          movesAway = self.board[a].get_seeds() + a
          if movesAway == 13:
            value += 2
          if self.board[a - 1].get_seeds() == 1 and self.board[(13 - a)%14].get_seeds() > 0 and not(self.board[a - 1].is_bank()):
            value += 1
          break
      before = self.board[13].get_seeds()
      self.play_move(testMove)
      after = self.board[13].get_seeds()
      value += after - before
      if self.board[12].get_seeds() == 1:
        value += 2 
      self.switch_player()
      test = ["T1", "T2", "T3", "T4", "T5", "T6"]
      bestAMove = 0
      seeds = [self.board[0].get_seeds(), self.board[1].get_seeds(), self.board[2].get_seeds(), self.board[3].get_seeds(), self.board[4].get_seeds(), self.board[5].get_seeds(), self.board[6].get_seeds(), self.board[7].get_seeds(), self.board[8].get_seeds(), self.board[9].get_seeds(), self.board[10].get_seeds(), self.board[11].get_seeds(), self.board[12].get_seeds(), self.board[13].get_seeds()]
      for j in range(len(self.get_valid_moves())):
        test[j] = Board(seeds)
        initial = test[j].board[6].get_seeds()
        testMove = self.get_valid_moves()[j]
        test[j].play_move(testMove)
        final = test[j].board[6].get_seeds()
        if final - initial > bestAMove:
          bestAMove = final - initial
      self.switch_player()
      value -= bestAMove
      return value
      
    def AI(self):
      test = ["Test1", "Test2", "Test3", "Test4", "Test5", "Test6"]
      seeds = [self.board[0].get_seeds(), self.board[1].get_seeds(), self.board[2].get_seeds(), self.board[3].get_seeds(), self.board[4].get_seeds(), self.board[5].get_seeds(), self.board[6].get_seeds(), self.board[7].get_seeds(), self.board[8].get_seeds(), self.board[9].get_seeds(), self.board[10].get_seeds(), self.board[11].get_seeds(), self.board[12].get_seeds(), self.board[13].get_seeds()]
      highestValue = -100
      move = 0 
      for i in range(len(self.get_valid_moves())):
        test[i] = Board(seeds)
        test[i].player = "B"
        testMove = self.get_valid_moves()[i]
        testValue = test[i].game_value(testMove)
        if testValue > highestValue:
          highestValue = testValue
          move = i
      print(f"Player B's move: {self.get_valid_moves()[move]}")
      self.play_move(self.get_valid_moves()[move])
     
def start_game():
  game = Board()

  mode = input("Do you want to play with another person or a computer. Type computer or person.\n")
  while not(mode.lower() == "computer") and not(mode.lower() == "person"):
      mode = input("That is not a valid input. Type computer or person.\n")

  if mode.lower() == "computer":
    difficulty = input("What mode do you want? Type easy or hard.\n")
    while not(difficulty.lower() == "easy") and not(difficulty.lower() == "hard"):
      difficulty = input("That is not a valid input. Type easy or hard.\n")
    print(game)
    while True:
      if game.player == "A":
        pit_choice = input(f"What Pit Player {game.player}?\n")
        while not(pit_choice in game.get_valid_moves()):
          pit_choice = input(f"Enter a correct input. What Pit Player {game.player}?\n")
        game.play_move(pit_choice)
      elif difficulty.lower() == "easy":
        game.computerPlayer()
      else:
        game.AI()
      print(game)
      if game.game_over():
        break
      game.switch_player()
    print(game.results()) 
  else:  
    print(game)
    while True:
      pit_choice = input(f"What Pit Player {game.player}?\n")
      while not(pit_choice in game.get_valid_moves()):
        pit_choice = input(f"Enter a correct input. What Pit Player {game.player}?\n")
      game.play_move(pit_choice)
      print(game)
      if game.game_over():
        break
      game.switch_player()
    print(game.results())  

start_game()