# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains the rounds of MotivationalQuoteAbciApp."""

from enum import Enum
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
)

from packages.elia.skills.your_fsm_app_abci.payloads import (
    CollectQuotePayload,
    FetchQuotePayload,
    SubmitQuotePayload,
    WaitForNextCyclePayload,
)


class Event(Enum):
    """MotivationalQuoteAbciApp Events"""

    DONE = "done"
    NO_MAJORITY = "no_majority"
    ROUND_TIMEOUT = "round_timeout"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class CollectQuoteRound(AbstractRound):
    """CollectQuoteRound"""

    payload_class = CollectQuotePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: CollectQuotePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CollectQuotePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class FetchQuoteRound(AbstractRound):
    """FetchQuoteRound"""

    payload_class = FetchQuotePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: FetchQuotePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: FetchQuotePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class SubmitQuoteRound(AbstractRound):
    """SubmitQuoteRound"""

    payload_class = SubmitQuotePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: SubmitQuotePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: SubmitQuotePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class WaitForNextCycleRound(AbstractRound):
    """WaitForNextCycleRound"""

    payload_class = WaitForNextCyclePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    # TODO: replace AbstractRound with one of CollectDifferentUntilAllRound,
    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError

    def check_payload(self, payload: WaitForNextCyclePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: WaitForNextCyclePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class MotivationalQuoteAbciApp(AbciApp[Event]):
    """MotivationalQuoteAbciApp"""

    initial_round_cls: AppState = FetchQuoteRound
    initial_states: Set[AppState] = {FetchQuoteRound}
    transition_function: AbciAppTransitionFunction = {
        FetchQuoteRound: {
            Event.DONE: CollectQuoteRound,
            Event.ROUND_TIMEOUT: FetchQuoteRound
        },
        CollectQuoteRound: {
            Event.DONE: SubmitQuoteRound,
            Event.NO_MAJORITY: FetchQuoteRound
        },
        SubmitQuoteRound: {
            Event.DONE: WaitForNextCycleRound
        },
        WaitForNextCycleRound: {
            Event.DONE: FetchQuoteRound
        }
    }
    final_states: Set[AppState] = set()
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        FetchQuoteRound: [],
    }
    db_post_conditions: Dict[AppState, Set[str]] = {

    }
