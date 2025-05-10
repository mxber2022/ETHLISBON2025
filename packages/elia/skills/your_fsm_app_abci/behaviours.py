# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#   Behaviours for MotivationalQuoteAbciApp
# ------------------------------------------------------------------------------

import requests
import time
from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.elia.skills.your_fsm_app_abci.models import Params
from packages.elia.skills.your_fsm_app_abci.models import (
    SynchronizedData,
    MotivationalQuoteAbciApp,
    CollectQuoteRound,
    FetchQuoteRound,
    SubmitQuoteRound,
    WaitForNextCycleRound,
)
from packages.elia.skills.your_fsm_app_abci.models import (
    CollectQuotePayload,
    FetchQuotePayload,
    SubmitQuotePayload,
    WaitForNextCyclePayload,
)


class MotivationalQuoteBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the motivational_quote_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        return cast(Params, super().params)


class FetchQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """FetchQuoteBehaviour"""

    matching_round: Type[AbstractRound] = FetchQuoteRound

    def async_act(self) -> Generator:
        """Perform fetching quote and send payload."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            try:
                response = requests.get("https://quotes.rest/qod?category=inspire")
                response.raise_for_status()
                quote = response.json()["contents"]["quotes"][0]["quote"]
            except Exception as e:
                self.context.logger.error(f"Failed to fetch quote: {e}")
                quote = "Keep pushing forward!"

            payload = FetchQuotePayload(sender=sender, content=quote)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CollectQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """CollectQuoteBehaviour"""

    matching_round: Type[AbstractRound] = CollectQuoteRound

    def async_act(self) -> Generator:
        """Perform consensus on the fetched quote."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            quote = self.synchronized_data.most_voted_quote
            payload = CollectQuotePayload(sender=sender, content=quote)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SubmitQuoteBehaviour(MotivationalQuoteBaseBehaviour):
    """SubmitQuoteBehaviour"""

    matching_round: Type[AbstractRound] = SubmitQuoteRound

    def async_act(self) -> Generator:
        """Perform submission of the agreed quote."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            quote = self.synchronized_data.agreed_quote
            payload = SubmitQuotePayload(sender=sender, content=quote)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class WaitForNextCycleBehaviour(MotivationalQuoteBaseBehaviour):
    """WaitForNextCycleBehaviour"""

    matching_round: Type[AbstractRound] = WaitForNextCycleRound

    def async_act(self) -> Generator:
        """Wait for the next cycle."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            wait_time = self.params.wait_time_in_seconds
            self.context.logger.info(f"Waiting {wait_time} seconds for next cycle.")
            time.sleep(wait_time)
            payload = WaitForNextCyclePayload(sender=sender, content="")

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class MotivationalQuoteRoundBehaviour(AbstractRoundBehaviour):
    """Wraps all round behaviours."""

    initial_behaviour_cls = FetchQuoteBehaviour
    abci_app_cls = MotivationalQuoteAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = {
        CollectQuoteBehaviour,
        FetchQuoteBehaviour,
        SubmitQuoteBehaviour,
        WaitForNextCycleBehaviour,
    }
