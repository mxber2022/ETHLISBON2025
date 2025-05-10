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

"""This package contains round behaviours of MotivationalQuoteAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.elia.skills.your_fsm_app_abci.models import Params
from packages.elia.skills.your_fsm_app_abci.rounds import (
    SynchronizedData,
    MotivationalQuoteAbciApp,
    CollectQuoteRound,
    FetchQuoteRound,
    SubmitQuoteRound,
    WaitForNextCycleRound,
)
from packages.elia.skills.your_fsm_app_abci.rounds import (
    CollectQuotePayload,
    FetchQuotePayload,
    SubmitQuotePayload,
    WaitForNextCyclePayload,
)


class MotivationalQuoteBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the your_fsm_app_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class CollectQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """CollectQuoteBehaviour"""

    matching_round: Type[AbstractRound] = CollectQuoteRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CollectQuotePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class FetchQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """FetchQuoteBehaviour"""

    matching_round: Type[AbstractRound] = FetchQuoteRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = FetchQuotePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SubmitQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """SubmitQuoteBehaviour"""

    matching_round: Type[AbstractRound] = SubmitQuoteRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SubmitQuotePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class WaitForNextCycleBehaviour(MotivationalQuoteBaseBehaviour):
    """WaitForNextCycleBehaviour"""

    matching_round: Type[AbstractRound] = WaitForNextCycleRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = WaitForNextCyclePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class MotivationalQuoteRoundBehaviour(AbstractRoundBehaviour):
    """MotivationalQuoteRoundBehaviour"""

    initial_behaviour_cls = FetchQuoteBehaviour
    abci_app_cls = MotivationalQuoteAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        CollectQuoteBehaviour,
        FetchQuoteBehaviour,
        SubmitQuoteBehaviour,
        WaitForNextCycleBehaviour
    ]
