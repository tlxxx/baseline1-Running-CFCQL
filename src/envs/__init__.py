from functools import partial
import sys
import os

from .multiagentenv import MultiAgentEnv

from .starcraft import StarCraft2Env
from .myenv import EqualLine,Consensus
from .gymma import GymmaWrapper

def __check_and_prepare_smac_kwargs(kwargs):
    assert "common_reward" in kwargs and "reward_scalarisation" in kwargs
    assert kwargs[
        "common_reward"
    ], "SMAC only supports common reward. Please set `common_reward=True` or choose a different environment that supports general sum rewards."
    del kwargs["common_reward"]
    del kwargs["reward_scalarisation"]
    assert "map_name" in kwargs, "Please specify the map_name in the env_args"
    return kwargs

def env_fn(env, **kwargs) -> MultiAgentEnv:
    return env(**kwargs)

def gymma_fn(**kwargs) -> MultiAgentEnv:
    # print(kwargs)
    # exit(0)
    # assert "common_reward" in kwargs and "reward_scalarisation" in kwargs
    return GymmaWrapper(**kwargs)


REGISTRY = {}
# REGISTRY["sc2"] = partial(env_fn, env=StarCraft2Env)
REGISTRY["equal_line"] = partial(env_fn, env=EqualLine)
REGISTRY["consensus"] = partial(env_fn, env=Consensus)
REGISTRY["gymma"] = gymma_fn

def register_smac():
    from .smac_wrapper import SMACWrapper

    def smac_fn(**kwargs) -> MultiAgentEnv:
        kwargs = __check_and_prepare_smac_kwargs(kwargs)
        return SMACWrapper(**kwargs)

    REGISTRY["sc2"] = smac_fn


def register_smacv2():
    from .smacv2_wrapper import SMACv2Wrapper

    def smacv2_fn(**kwargs) -> MultiAgentEnv:
        kwargs = __check_and_prepare_smac_kwargs(kwargs)
        return SMACv2Wrapper(**kwargs)

    REGISTRY["sc2v2"] = smacv2_fn

if sys.platform == "linux":
    os.environ.setdefault("SC2PATH", "~/StarCraftII")
