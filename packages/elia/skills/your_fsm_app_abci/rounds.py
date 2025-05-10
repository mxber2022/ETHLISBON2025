# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#   Rounds for MotivationalQuoteAbciApp
# ------------------------------------------------------------------------------

from enum import Enum
from typing import Dict, FrozenSet, Set, Type

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AppState,
    BaseSynchronizedData,
    CollectSameUntilThresholdRound,
    EventToTimeout,
)

from packages.elia.skills.your_fsm_app_abci.payloads import (
    CollectQuotePayload,
    FetchQuotePayload,
    SubmitQuotePayload,
    WaitForNextCyclePayload,
)


class Event(Enum):
    """Events for FSM transitions."""
    DONE = "done"
    NO_MAJORITY = "no_majority"
    ROUND_TIMEOUT = "round_timeout"


class SynchronizedData(BaseSynchronizedData):
    """Synchronized data shared across the rounds."""
    @property
    def most_voted_quote(self) -> str:
        return self.most_voted_payload  # type: ignore

    @property
    def agreed_quote(self) -> str:
        return self.most_voted_payload  # type: ignore


class FetchQuoteRound(CollectSameUntilThresholdRound):
    """Round where agents fetch and submit the quote."""
    payload_class = FetchQuotePayload
    payload_attribute = "quote"
    synchronized_data_class = SynchronizedData


class CollectQuoteRound(CollectSameUntilThresholdRound):
    """Round where agents reach consensus on a quote."""
    payload_class = CollectQuotePayload
    payload_attribute = "quote"
    synchronized_data_class = SynchronizedData


class SubmitQuoteRound(CollectSameUntilThresholdRound):
    """Round to submit the quote to the blockchain."""
    payload_class = SubmitQuotePayload
    payload_attribute = "quote"
    synchronized_data_class = SynchronizedData


class WaitForNextCycleRound(CollectSameUntilThresholdRound):
    """Pause state before restarting the FSM."""
    payload_class = WaitForNextCyclePayload
    payload_attribute = "ack"
    synchronized_data_class = SynchronizedData


class MotivationalQuoteAbciApp(AbciApp[Event]):
    """The FSM App definition for the Motivational Quote Agent."""

    initial_round_cls: AppState = FetchQuoteRound
    initial_states: Set[AppState] = {FetchQuoteRound}
    transition_function: AbciAppTransitionFunction = {
        FetchQuoteRound: {
            Event.DONE: CollectQuoteRound,
            Event.ROUND_TIMEOUT: FetchQuoteRound,
        },
        CollectQuoteRound: {
            Event.DONE: SubmitQuoteRound,
            Event.NO_MAJORITY: FetchQuoteRound,
        },
        SubmitQuoteRound: {
            Event.DONE: WaitForNextCycleRound,
        },
        WaitForNextCycleRound: {
            Event.DONE: FetchQuoteRound,
        },
    }
    final_states: Set[AppState] = set()
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {FetchQuoteRound: set()}
    db_post_conditions: Dict[AppState, Set[str]] = {}
