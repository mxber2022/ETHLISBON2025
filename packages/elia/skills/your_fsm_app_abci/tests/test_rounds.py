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

"""This package contains the tests for rounds of MotivationalQuote."""

from typing import Any, Type, Dict, List, Callable, Hashable, Mapping
from dataclasses import dataclass, field

import pytest

from packages.elia.skills.your_fsm_app_abci.payloads import (
    CollectQuotePayload,
    FetchQuotePayload,
    SubmitQuotePayload,
    WaitForNextCyclePayload,
)
from packages.elia.skills.your_fsm_app_abci.rounds import (
    AbstractRound,
    Event,
    SynchronizedData,
    CollectQuoteRound,
    FetchQuoteRound,
    SubmitQuoteRound,
    WaitForNextCycleRound,
)
from packages.valory.skills.abstract_round_abci.base import (
    BaseTxPayload,
)
from packages.valory.skills.abstract_round_abci.test_tools.rounds import (
    BaseRoundTestClass,
    BaseOnlyKeeperSendsRoundTest,
    BaseCollectDifferentUntilThresholdRoundTest,
    BaseCollectSameUntilThresholdRoundTest,
 )


@dataclass
class RoundTestCase:
    """RoundTestCase"""

    name: str
    initial_data: Dict[str, Hashable]
    payloads: Mapping[str, BaseTxPayload]
    final_data: Dict[str, Hashable]
    event: Event
    synchronized_data_attr_checks: List[Callable] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


MAX_PARTICIPANTS: int = 4


class BaseMotivationalQuoteRoundTest(BaseRoundTestClass):
    """Base test class for MotivationalQuote rounds."""

    round_cls: Type[AbstractRound]
    synchronized_data: SynchronizedData
    _synchronized_data_class = SynchronizedData
    _event_class = Event

    def run_test(self, test_case: RoundTestCase) -> None:
        """Run the test"""

        self.synchronized_data.update(**test_case.initial_data)

        test_round = self.round_cls(
            synchronized_data=self.synchronized_data,
        )

        self._complete_run(
            self._test_round(
                test_round=test_round,
                round_payloads=test_case.payloads,
                synchronized_data_update_fn=lambda sync_data, _: sync_data.update(**test_case.final_data),
                synchronized_data_attr_checks=test_case.synchronized_data_attr_checks,
                exit_event=test_case.event,
                **test_case.kwargs,  # varies per BaseRoundTestClass child
            )
        )


class TestCollectQuoteRound(BaseMotivationalQuoteRoundTest):
    """Tests for CollectQuoteRound."""

    round_class = CollectQuoteRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestFetchQuoteRound(BaseMotivationalQuoteRoundTest):
    """Tests for FetchQuoteRound."""

    round_class = FetchQuoteRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestSubmitQuoteRound(BaseMotivationalQuoteRoundTest):
    """Tests for SubmitQuoteRound."""

    round_class = SubmitQuoteRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestWaitForNextCycleRound(BaseMotivationalQuoteRoundTest):
    """Tests for WaitForNextCycleRound."""

    round_class = WaitForNextCycleRound

    # TODO: provide test cases
    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)

