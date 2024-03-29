"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math
import numpy as np

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def get_distance_between_players(game, player):
    """
    Calculates the distance between players by adding up the
    absolute difference between their locations on the
    horizontal and vertical column/rows
    """
    opponent = game.get_opponent(player)
    loc = game.get_player_location(player)
    opponent_loc = game.get_player_location(opponent)
    if loc is None or opponent_loc is None:
        return 0.
    return abs(loc[0] - opponent_loc[0]) + abs(loc[1] - opponent_loc[1])

def get_distance_from_center(game, player):
    """
    Provides the negative distance from center
    Expessed as number of cells from center along the column
    added to the number of cells along the column
    """
    loc = game.get_player_location(player)
    if loc is None:
        return 0.
    dist_from_vertical_center = abs(game.height/2. - loc[0])
    dist_from_horizontal_center = abs(game.width/2. - loc[1])
    return dist_from_vertical_center + dist_from_horizontal_center

def get_diff_player_moves(game, player):
    """
    Returns the difference between player's moves and the opponents moves
    """
    num_moves = len(game.get_legal_moves(player))
    opponent_num_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return num_moves - opponent_num_moves

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # features
    moves_own = len(game.get_legal_moves(player))
    moves_opp = len(game.get_legal_moves(game.get_opponent(player)))
    board = game.height * game.width
    moves_board = game.move_count / board
    if moves_board > 0.33:
        move_diff = (moves_own - moves_opp * 2) 
    else:
        move_diff = (moves_own - moves_opp)

    pos_own = game.get_player_location(player)
    pos_opp = game.get_player_location(game.get_opponent(player))

    m_distance = abs(pos_own[0] - pos_opp[0]) + abs(pos_own[1] - pos_opp[1])
    return float(move_diff / m_distance)

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # features
    diff_moves = get_diff_player_moves(game, player)
    distance_from_center = get_distance_from_center(game, player)
    distance_between_players = get_distance_between_players(game, player)
    features = [diff_moves, distance_from_center, distance_between_players]
    # separate the weights into a weight matrix so we can 
    # easily modify them and operate on them using matrix multiplication
    weights = [2.2, -1.2, -0.5]
    return np.matmul(features, weights)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # features
    moves_own = len(game.get_legal_moves(player))
    moves_opp = len(game.get_legal_moves(game.get_opponent(player)))
    return float(moves_own - moves_opp * 2)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=19.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.num_nodes_visited = 0


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def cutoff_test(self, game, player, current_depth):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
        self.num_nodes_visited += 1
        player_moves = len(game.get_legal_moves(player))
        opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return current_depth == 0 or (player_moves == 0 and opponent_moves == 0)

    def min_value(self, game, current_depth):
        """ 
        At this level, The following condition holds true:
        game.active_player == game._player_2

        Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.cutoff_test(game, game._player_1, current_depth):
            # if game is over and we're trying to minimize
            # return +1, because the min has lost
            # since we define "winning" as having an extra move
            return self.score(game, game._player_1)

        v = float("inf")
        for move in game.get_legal_moves():
            next_state = game.forecast_move(move)
            next_state_value = self.max_value(next_state, current_depth - 1)
            v = min(v, next_state_value)
        return v

    def max_value(self, game, current_depth):
        """ 
        At this level, The following condition holds true:
        game.active_player == game._player_1

        Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.cutoff_test(game, game._player_1, current_depth):
            # if game is over and we're trying to maximize
            # return -1, because the max has lost
            # since we define "winning" as having an extra move
            return self.score(game, game._player_1)
        
        v = float("-inf")
        for move in game.get_legal_moves():
            next_state = game.forecast_move(move)
            next_state_value = self.min_value(next_state, current_depth - 1)
            v = max(v, next_state_value)
        return v

    def minimax(self, game, depth_limit):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        max_value = float("-inf")
        best_move = (-1, -1)
        for move in game.get_legal_moves():
            next_state = game.forecast_move(move)
            decision_value = self.min_value(next_state, depth_limit - 1)
            if decision_value > max_value:
                max_value = decision_value
                best_move = move
                
        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
        
    def cutoff_test(self, game, player, current_depth):
        """ 
        Return True if depth limit is reached or 
        there are no more moves available to be played
        """
        player_moves = len(game.get_legal_moves(player))
        opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return current_depth == 0 or (player_moves == 0 and opponent_moves == 0)

    def min_value(self, game, move, alpha, beta, current_depth):
        """ 
        Implements the "minimizer" helper function from 
        the AIMA ALPHA-BETA-SEARCH algorithm,

        The function is modified to also return the "worst_move" in addition
        to the value. 
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.cutoff_test(game, game._player_1, current_depth):
            return self.score(game, game._player_1), move

        v = float("inf")
        worst_move = (-1, -1)
        for legal_move in game.get_legal_moves():
            next_state = game.forecast_move(legal_move)
            next_state_value, _ = self.max_value(next_state, legal_move, alpha, beta, current_depth - 1)
            if next_state_value < v:
                v = next_state_value
                worst_move = legal_move
            if v <= alpha: 
                return v, worst_move
            beta = min(beta, v)
        return v, worst_move

    def max_value(self, game, move, alpha, beta, current_depth):
        """ 
        Implements the "maximizer" helper function from 
        the AIMA ALPHA-BETA-SEARCH algorithm

        The function is modified to also return the "best_move" in addition
        to the value. 
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.cutoff_test(game, game._player_1, current_depth):
            return self.score(game, game._player_1), move
        
        v = float("-inf")
        best_move = (-1, -1)
        for legal_move in game.get_legal_moves():
            next_state = game.forecast_move(legal_move)
            next_state_value, _ = self.min_value(next_state, legal_move, alpha, beta, current_depth - 1)
            if next_state_value > v:
                v = next_state_value
                best_move = legal_move
            if v >= beta: 
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    def alphabeta(self, game, depth_limit, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        value, best_move = self.max_value(game, (-1,-1), alpha, beta, depth_limit)
        return best_move

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        try:
            depth_limit = 1
            while True: # iterative deepning, search with increasing depth_limit on each loop
                best_move = self.alphabeta(game, depth_limit)
                depth_limit += 1
        except SearchTimeout:
            pass

        # if there are legal moves left, avoid a forefit and continue playing 
        if best_move == (-1, -1):
            legal_moves = game.get_legal_moves()
            if len(legal_moves) > 0:
                return legal_moves[0]

        return best_move

    def get_testable_move(self, game, time_left, depth_limit):
        """
        Testable alphabeta method
        """
        self.time_left = time_left
        return self.alphabeta(game, depth_limit)
