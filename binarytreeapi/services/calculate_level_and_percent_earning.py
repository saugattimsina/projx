def calculate_percent_level_quick_start(rank):
    if rank == "Pawn":
        percentage = 50
        level = 1
    elif rank == "Knight":
        percentage = 60
        level = 2
    elif rank == "Bishop":
        percentage = 65
        level = 4
    elif rank == "Rook":
        percentage = 70
        level = 6
    elif rank == "Queen":
        percentage = 78
        level = 8
    elif rank == "King":
        percentage = 80
        level = 10

    return percentage, level


def calculate_percent_level_matrix(rank):
    if rank == "Pawn":
        percentage = 48
        level = 12
    elif rank == "Knight":
        percentage = 52
        level = 13
    elif rank == "Bishop":
        percentage = 52
        level = 13
    elif rank == "Rook":
        percentage = 56
        level = 14
    elif rank == "Queen":
        percentage = 56
        level = 14
    elif rank == "King":
        percentage = 60
        level = 15

    return percentage, level


def circle_network_residual_pool_bonus(rank):
    if rank == "Pawn":
        percentage = 0
    elif rank == "Knight":
        percentage = 10
    elif rank == "Bishop":
        percentage = 15
    elif rank == "Rook":
        percentage = 17
    elif rank == "Queen":
        percentage = 20
    elif rank == "King":
        percentage = 38

    return percentage


def calculate_trading_profit_level_percentage(rank):
    if rank == "Pawn":
        percentage = 8
        level = 1
    elif rank == "Knight":
        percentage = 11
        level = 3
    elif rank == "Bishop":
        percentage = 15
        level = 5
    elif rank == "Rook":
        percentage = 21
        level = 6
    elif rank == "Queen":
        percentage = 28
        level = 8
    elif rank == "King":
        percentage = 40
        level = 10

    return percentage, level
