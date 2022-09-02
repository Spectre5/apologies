# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Reward calculations.

Version 1 of the reward algorithm was developed by hand following my own mental model for the
strength of a position.  I used the spreadsheet found in notes/reward.xlsx to refine my
thoughts as I developed the algorithm.

Basically, a pawn is worth more the closer it is to home.  It's worth incrementally more in the
safe zone (where it can't be hurt).  There's an additional bonus for winning, to incentivize
the engine to pick a move that ends the game as fast as possible.  The score is calculated by
comparing the player's position relative to the positions of all its opponents.  We want the
engine to pick the move that both maximizes the player's position and also minimizes the
positions of its opponents.

In simulation runs generated by simulation.py, a reward-based character source vastly out
performs a source that picks its moves randomly.  The worst-case scenario is a 4-player
STANDARD mode game between a single reward-based source and 3 random sources, where the
reward-based source wins about 70% of the time.  This is probably because in a STANDARD mode
game, the possible moves in each turn are fairly limited, due to each player picking and
playing the top card off the deck.  This evens the playing field, because it's quite likely
that any player will have no good move on their turn.  In a 4-player ADULT mode game, where the
engine has the opportunity to choose between more possible moves for each turn, a reward-based
source wins more than 98% of the time against 3 random sources. 
"""

from abc import ABC, abstractmethod
from typing import Tuple

from .game import Player, PlayerView
from .rules import BoardRules


class RewardCalculator(ABC):

    """Abstract reward calculator interface, to support multiple reward implementations."""

    @abstractmethod
    def calculate(self, view: PlayerView) -> float:
        """Calculate the reward associated with a player view."""

    @abstractmethod
    def range(self, players: int) -> Tuple[float, float]:
        """Return the range of possible rewards for a game."""


class RewardCalculatorV1(RewardCalculator):
    """Version 1 of the reward calculator."""

    def calculate(self, view: PlayerView) -> float:
        """Calculate the reward associated with an observation."""
        return float(RewardCalculatorV1._reward(view))

    def range(self, players: int) -> Tuple[float, float]:
        """Return the range of possible rewards for a game."""
        return 0.0, float((players - 1) * 400)  # reward is up to 400 points per opponent

    @staticmethod
    def _reward(view: PlayerView) -> int:
        # Reward measures this player's overall game position relative to their opponents
        player_score = RewardCalculatorV1._player_score(view.player)
        opponent_scores = [RewardCalculatorV1._player_score(player) for player in view.opponents.values()]
        reward = (len(view.opponents) * player_score) - sum(opponent_scores)
        return 0 if reward < 0 else reward

    @staticmethod
    def _player_score(player: Player) -> int:
        # There are 3 different incentives, designed to encourage the right behavior
        distance_incentive = RewardCalculatorV1._distance_incentive(player)
        safe_incentive = RewardCalculatorV1._safe_incentive(player)
        winner_incentive = RewardCalculatorV1._winner_incentive(player)
        return distance_incentive + safe_incentive + winner_incentive

    @staticmethod
    def _distance_incentive(player: Player) -> int:
        # Incentive of 1 point for each square closer to home for each of the player's 4 pawns
        distance = sum(BoardRules.distance_to_home(pawn) for pawn in player.pawns)
        return 260 - distance  # 260 = 4*65, max distance for 4 pawns

    @staticmethod
    def _safe_incentive(player: Player) -> int:
        # Incentive of 10 points for each pawn in safe or home
        return sum(10 if pawn.position.home or pawn.position.safe is not None else 0 for pawn in player.pawns)

    @staticmethod
    def _winner_incentive(player: Player) -> int:
        # Incentive of 100 points for winning the game
        return 100 if player.all_pawns_in_home() else 0
