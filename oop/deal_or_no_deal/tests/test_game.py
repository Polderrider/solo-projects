import pytest
from unittest.mock import patch

from game import Game, Box, Round, Player

def test_setup_boxes():
    """ 
    ensure private method setup boxes delivers the following crtieria
    1. boxes held in dict
    2. box numbers and values are unique
    3. 22 box objects extist
    4. a box object has 2 attributes
    5. the final values are not in ascending order
      
    Note, don't call _setup_boxes() directly in the test
    Only test the private method's output which lives on the instance of the class. eg game = Game()
    accpeted approach for testing private methods — 
        test the result through the public interface, not the method itself.
    """
    # arrange
    game = Game()
    boxes = game.boxes

    # act
    length = len(game.boxes)
    
    numbers = set()
    values = set()
    for key, box in game.boxes.items():
        numbers.add(key)
        values.add(box.value)

    assert isinstance(game.boxes, dict)
    assert all(isinstance(single_box, Box) for single_box in game.boxes.values())     # SNIPPETS test-assert-all()-generator expression passed to all(). returns True only if every element satisfies the condition. 

    assert length == 22
    assert len(numbers) == 22
    assert len(values) == 22


def test_setup_rounds():
    """ 
    instance game = Game() sees self.rounds instantiate in init

    private method returns a list type
    how many rounds are there
    total number of turns == 20 
    
    how many turns are there per round
    round list elements are a Round object
       
    """

    # arrange
    game = Game()

    # act
    round_count = len(game.rounds)

    turns_per_round = []
    total_turns = 0
    for round in game.rounds:
        total_turns += round.turns
        turns_per_round.append(round.turns)

    # assert
    assert isinstance(game.rounds, list)
    assert round_count == 7
    assert total_turns == 20
    assert turns_per_round == [5,4,3,3,2,2,1]
    assert all(isinstance(round, Round) for round in game.rounds)


def test_setup_player():
    game = Game()
    expected = 'John'
    with patch('builtins.input', return_value=expected):
        player = game._setup_player()

    assert player.name == expected
    assert isinstance(player.name, str)
    assert isinstance(player, Player)


def test_get_valid_box():
   
    game = Game()
    expected = "1"

    with patch('builtins.input', return_value=expected):
        box_number = game._get_valid_box("1")
    

    assert box_number.number == expected
    assert isinstance(box_number, Box)


def test_get_valid_box_raises_error():
    """Test expected failures"""

    game = Game()

    with patch('builtins.input', side_effect=["99", "1"]):  # SNIPPETS test-patch-input-simulate invalid/valid input() to return different values on successive calls. patch uses 'side_effect' instead of return_value.
        box = game._get_valid_box("Choose a box number to play game: ")

    assert isinstance(box, Box)
    assert box.number == "1"


def test_remove_value_from_board():

    game = Game()

    game.remaining_values = ["1p"]

    game._remove_value_from_board("1p")

    assert game.remaining_values == ["_"]
    

def test_get_last_box():
    game = Game()
    game.boxes = {"1": Box("1", "1p")}

    obj = game._get_last_box()

    assert isinstance(obj, Box)
    assert obj.number == "1"
    assert obj.value == "1p"


def test_offer_swap_answer_y():
    pass


def test_offer_swap_answer_n():
    pass
