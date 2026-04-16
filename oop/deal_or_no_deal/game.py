import random
import decimal # nb: usually not a good idea to use floats for monetary values, use decimal to avoid rounding errors.

""" 
Deal or no deal gameshow - see README.md
 
Unfamiliar oop concepts used:
1. object composition
introduced the passing of a class's instance as a parameter 
to another class. 
eg 

2. methods as Conductors
Game.run() is a conductor, not a performer, because it only 
calls other methods and objects that actually handle the detail

notes
SNIPPETS create-deepcopy-slice-listname[:]

"""


class Box:
    
    def __init__(self, number, value):
        self.number = number
        self.value = value

    def __repr__(self):
        return f"<Box {self.number}: {self.value}>"
        
    def _display_closed_box_number(self) -> str:
        return self.number
    
    def _reveal_opened_box_value(self):
        return self.value


class Player:
    
    def __init__(self, name):
        self.name = name
        self.box = None     


class Round:
    
    def __init__(self, turns, game):
        self.turns = turns
        self.game = game
    

    def run(self):

        while self.turns != 0:

            self.game._display_remaining_box_numbers()
            self.game._display_remaining_box_values()

            removed_value = self._process_player_turn()     
            self.game._remove_value_from_board(removed_value)
            
            self.turns -= 1
        
        self.game._banker_offer()


    def _process_player_turn(self):
        """ reveals the cash value inside a box that was picked by the player """

        removed_box = self.game._get_valid_box("Select a box number to open: ")
        print(f"You selected Box {removed_box.number}. There was {removed_box.value} inside.")
        return removed_box.value


class Game:

    def __init__(self):
        self.remaining_values = None
        self.boxes = self._setup_boxes()
        self.rounds = self._setup_rounds()
        self.player = None


    def run(self):
    
        self._print_game_instructions() 
        self.player = self._setup_player()
        self.player.box = self._assign_player_box()
        for r in self.rounds:
            r.run()
        self._offer_swap()
        self._reveal_result()
        

    def _print_game_instructions(self):
        print("these are the instructions") 
     

    def _setup_player(self):
        
        name = input("Enter your name: ")
        return Player(name)


    def _setup_boxes(self):

        values = "1p, 10p, 50p, £1, £5, £10, £50, £100, £250, £500, £750, £1,000, £3,000, £5,000, £10,000, £15,000, £20,000, £35,000, £50,000, £75,000, £100,000, £250,000"
        self.remaining_values = values.split(", ")
        box_values = self.remaining_values[:]   

        game_boxes = {}
        random.shuffle(box_values)
        length = len(box_values)

        for i in range(0, length):
            number = str(i+1)
            box = Box(number, box_values[i])
            game_boxes[number] = box
        
        return game_boxes


    def _setup_rounds(self):
        round_structure = {1: 5, 2: 4, 3: 3, 4: 3, 5: 2, 6: 2, 7: 1}

        rounds = []     # a list of Round objects. Round(turns, instance of game referred to as self) passing instance of self to Round class allows instances of round to round.game.game_methods()
        for _, turns in round_structure.items():
            r = Round(turns, self)
            rounds.append(r)
        return rounds


    def _assign_player_box(self):
        box = self._get_valid_box("Choose a box number to play game: ")
        return box


    def _display_remaining_box_numbers(self):
        for box in self.boxes.values():
            print(box.number)
        

    def _display_remaining_box_values(self):
        for value in self.remaining_values:
            print(value)

    
    def _remove_value_from_board(self, removed):
      
        for i in range(len(self.remaining_values)):
            if self.remaining_values[i] == removed:
                self.remaining_values[i] = "_"
    

    def _get_valid_box(self, prompt):

        removed = None
        while not removed:
            try:
                selected_number = input(prompt)                  
                removed = self.boxes.pop(selected_number)        
            except KeyError:                                
                    print(f"Box {selected_number} is not available. Choose again.")
        return removed                                      


    def _get_last_box(self):
        keys = list(self.boxes.keys())
        last_key = keys[0]              # TODO redundant because dict.pop() returns last key by default
        return self.boxes.pop(last_key)


    def _banker_offer(self):
        

        # TODO: banker offer at end of round 
        # eg 10% of highest cash value left

        amount = 0
        for box in self.boxes.values():

            value = self._convert_int(box.value)
            amount = max(amount, value)

        raw = decimal.Decimal(0.1) * amount
        offer = "£{:,}".format(round(raw,0))
        answer = input(f"The banker wants to offer you {offer}. Do you accept? y/n")
        if answer == 'y':
            print(f"Congratulations! You have won {offer}.")
            if offer > self.player.box.value:
                print(f"Lucky you. If you had kept your box, you would have won {self.player.box.value}")
            else:
                print(f"Oh no! Your box had {self.player.box.value}")

        # TODO start here: happy path implemented. add try/except offer decision input().



    def _convert_int(self, cash_str):
        new_str = ""
        for char in cash_str:
            if char not in ['£', 'p', ',']:
                new_str += char
        return int(new_str)






    def _offer_swap(self):

        # offer player the chance to swap box with last box
        last_two_values = []
        for value in self.remaining_values:
            if value != "_":
                last_two_values.append(value)

        print(f"There are two values left: {last_two_values[0]} and {last_two_values[1]}")

        decision = input("Do you want to swap your box with the last game box? (y/n): ")
        if decision.lower() == 'y':
            self._swap_player_box()


    def _swap_player_box(self):
        original = self.player.box
        self.player.box = self._get_last_box()
        return original


    def _reveal_result(self):
        result = self.player.box.value
        print(f"You have won {result}")






# --Entry Point------------------------------------

if __name__ == "__main__":
    game = Game()
    game.run()

    
  