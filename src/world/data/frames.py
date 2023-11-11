"""
Frame sequence source modules.
"""
from typing import List
from pygame import Surface

from src.registry import RegistryUtil
from src.world.data.registries import Registries
from src.world.data.tiles import Tiles


def register(path: str, frames: List[Surface]):
    """
    Register a frame sequence.
    :param path: The path of the frame sequence.
    :param frames: A sequence of surfaces.
    :return: The animation.
    """
    return Registries.FrameSequence.register(RegistryUtil.createRegistry(path), frames)


class Frames:
    """
    Animation fame resources.
    """

    Water = register("water", [Tiles.Water0, Tiles.Water1, Tiles.Water2, Tiles.Water3])
