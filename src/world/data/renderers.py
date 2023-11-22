"""
Renderer resource module.
"""

from src.registry import RegistryUtil
from src.world.data.registries import Registries
from src.world.renderer import Renderer, GrassRenderer, HouseRenderer


def register(path: str, renderer: Renderer.__subclasses__()) -> Renderer.__subclasses__():
    """
    Register a renderer.
    :param path: The path of the renderer.
    :param renderer: The renderer to register.
    """
    return Registries.Renderer.register(RegistryUtil.createRegistry(path), renderer)


class Renderers:
    """
    Renderer resources.
    """

    House: HouseRenderer = register("house", GrassRenderer())
    Grass: GrassRenderer = register("grass", GrassRenderer())
