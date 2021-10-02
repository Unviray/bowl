from src.main import Game, sum_next_move


def test_sum_next_move():
    frame = [[8, 1, 1], [8, "SPARE"], [1, 2, None], None, None]
    assert sum_next_move(frame, index=1, n=2) == 3

    frame = [[8, 1, 1], [8, "SPARE"], [4, None, None], None, None]
    assert sum_next_move(frame, index=1, n=2) == 4

    frame = [[8, 1, 1], ["STRIKE"], [4, "SPARE"], None, None]
    assert sum_next_move(frame, index=1, n=3) == 19


def test_game():
    game = Game()

    # Frame 1 Scored 10
    game.launch(8)
    game.launch(1)
    game.launch(1)
    assert game.current_score == 10

    # Frame 2 Scored 15
    game.launch(8)
    game.launch(7)
    assert game.current_score == 25

    # Frame 3 Scored 4
    game.launch(1)
    game.launch(2)
    game.launch(1)
    assert game.current_score == 32

    # Frame 4 Scored 15
    game.launch(15)
    assert game.current_score == 47

    # Frame 5 Scored 4
    game.launch(1)
    game.launch(2)
    game.launch(1)
    assert game.current_score == 55

    # Frame (OutOfBound) Scored 0
    game.launch(3)
    assert game.current_score == 55


def test_game2():
    game = Game()

    # Scored 15
    game.launch(15)

    # Scored 11
    game.launch(8)
    game.launch(1)
    game.launch(2)

    # Scored 15
    game.launch(1)
    game.launch(2)
    game.launch(12)

    # Scored 11
    game.launch(6)
    game.launch(4)
    game.launch(1)

    # Scored 28
    game.launch(15)
    game.launch(8)
    game.launch(2)
    game.launch(3)

    assert game.current_score == 101


def test_game_full():
    game = Game()

    game.launch(15)
    assert game.current_score == 15

    game.launch(15)
    assert game.current_score == (30 + 15)

    game.launch(15)
    assert game.current_score == (45 + 30 + 15)

    game.launch(15)
    assert game.current_score == (60 + 45 + 30 + 15)

    game.launch(15)
    game.launch(15)
    game.launch(15)
    game.launch(15)
    assert game.current_score == 300
