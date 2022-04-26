from abc import ABC, abstractmethod
from typing import List
from agent import Agent


class IntelAction(ABC):
    """Abstract class for intelligence/counterintelligence actions"""
    def __init__(self, attacker: Agent, target: Agent, reflexion_level: int):
        """
        :param attacker: Agent
        :param target: Agent
        :param reflexion_level: int
        """
        self.attacker = attacker
        self.target = target
        self.reflexion_level = reflexion_level

    @abstractmethod
    def run_action(self):
        """Actual execution of specific action"""
        pass


class GetInfo(IntelAction):
    """
    Intelligence getting info action. The success of this action depends on attacker's and target's intelligence levels.
    If attacker has higher intel level, he gets information. If intel levels are the same for both agents, attacker does
    not get info (simulation of defence). If target's intel level is higher, then the attacker is being disinformed.
    """
    def __init__(self, id_getinfo_agent: int = None, *args, **kwargs):
        """
        :param attacker: Agent
        :param target: Agent
        :param reflexion_level: int
        :param id_getinfo_agent: int
        """
        self.id_getinfo_agent = id_getinfo_agent
        super().__init__(*args, **kwargs)

    def run_action(self) -> None:
        # Agent's ids preparation
        ids_for_getinfo = [self.id_getinfo_agent] if self.id_getinfo_agent is not None else []
        ids_for_modify = [self.target.id_number, self.id_getinfo_agent]

        # Information (target's awareness structure element)
        intercepted_info = self.target.get_awareness_info(self.reflexion_level - 1, ids_for_getinfo)

        # If information is None, then it means that target has no such reflexion level - nothing happens
        if intercepted_info is not None:
            if self.attacker.intel_level > self.target.intel_level:
                # Successfully completed intelligence action
                self.attacker.modify_awareness_structure(self.reflexion_level, ids_for_modify, intercepted_info)
            elif self.attacker.intel_level == self.target.intel_level:
                # Failed intelligence action - successful defence
                pass
            else:
                # Failed intelligence action - successful counterintelligence action
                counter_disinformation = intercepted_info
                counter_disinformation = [int(x * self.target.game.disinformation_factor) for x in
                                          counter_disinformation]
                self.attacker.modify_awareness_structure(self.reflexion_level, ids_for_modify, counter_disinformation)
        else:
            pass


class Disinform(IntelAction):
    """
    Counterintelligence disinforming action. The success of this action depends on attacker's and target's intelligence
    levels. If attacker has higher intel level, he changes target's awareness structure. If intel levels are the same
    for both agents, target's awareness structure is not changed (simulation of defence). If target's intel level is
    higher, then the attacker's awareness structure is changed (he thinks his disinformation was successful) but the
    target's awareness structure is not changed.
    """
    def __init__(self, ids_disinform_agent: List[int] = None, *args, **kwargs):
        self.ids_disinform_agent = ids_disinform_agent
        super().__init__(*args, **kwargs)

    def run_action(self) -> None:
        ids_for_getinfo = self.ids_disinform_agent

        value = self.target.get_awareness_info(self.reflexion_level, ids_for_getinfo)
        value = [int(val * self.target.game.disinformation_factor) for val in value]

        if value is not None and self.attacker.intel_level > self.target.intel_level:
            self.target.modify_awareness_structure(self.reflexion_level, ids=ids_for_getinfo, values=value)
            self.attacker.modify_after_disinform(self.reflexion_level - 1, value, self.target.id_number,
                                                 ids_for_getinfo)
        elif value is not None and self.attacker.intel_level == self.target.intel_level:
            pass
        elif value is not None:
            self.attacker.modify_after_disinform(self.reflexion_level - 1, value, self.target.id_number,
                                                 ids_for_getinfo)
