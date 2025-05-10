# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#   Payloads for MotivationalQuoteAbciApp
# ------------------------------------------------------------------------------

from dataclasses import dataclass
from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


@dataclass(frozen=True)
class CollectQuotePayload(BaseTxPayload):
    """Transaction payload for the CollectQuoteRound."""
    content: str


@dataclass(frozen=True)
class FetchQuotePayload(BaseTxPayload):
    """Transaction payload for the FetchQuoteRound."""
    content: str


@dataclass(frozen=True)
class SubmitQuotePayload(BaseTxPayload):
    """Transaction payload for the SubmitQuoteRound."""
    content: str


@dataclass(frozen=True)
class WaitForNextCyclePayload(BaseTxPayload):
    """Transaction payload for the WaitForNextCycleRound."""
    content: str
