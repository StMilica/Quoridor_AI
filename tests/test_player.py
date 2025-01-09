from quoridor.src.player import Player

def test_player_initialization():
    player = Player("Player 1", (0, 4), 8)
    assert player.name == "Player 1"
    assert player.position == (0, 4)
    assert player.goal_row == 8
    assert player.walls_remaining == 10

def test_player_move():
    player = Player("Player 1", (0, 4), 8)
    player.move((1, 4))
    assert player.position == (1, 4)

def test_player_use_wall():
    player = Player("Player 1", (0, 4), 8)
    player.use_wall()
    assert player.walls_remaining == 9

def test_player_no_walls_left():
    player = Player("Player 1", (0, 4), 8)
    player.walls_remaining = 0
    try:
        player.use_wall()
    except ValueError as e:
        assert str(e) == "Player 1 has no walls remaining."
