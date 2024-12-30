from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from cython_extensions import cy_distance_to
from sc2.position import Point2
from sc2.unit import Unit

from ares.behaviors.combat.individual.combat_individual_behavior import (
    CombatIndividualBehavior,
)
from ares.managers.manager_mediator import ManagerMediator

if TYPE_CHECKING:
    from ares import AresBot


@dataclass
class PathUnitToTarget(CombatIndividualBehavior):
    """Path a unit to its target destination.

    TODO: Add attack enemy in range logic / parameter
        Not added yet since that may be it's own Behavior

    Example:
    ```py
    from ares.behaviors.combat import PathUnitToTarget

    unit: Unit
    grid: np.ndarray = self.mediator.get_ground_grid
    target: Point2 = self.game_info.map_center
    self.register_behavior(PathUnitToTarget(unit, grid, target))
    ```

    Attributes:
        unit: The unit to path.
        grid: 2D grid to path on.
        target: Target destination.
        success_at_distance: If the unit has gotten this close, consider path
            behavior complete. Defaults to 0.0.
        sensitivity: Path precision. Defaults to 5.
        smoothing: Whether to smooth out the path. Defaults to False.
        sense_danger: Whether to check for dangers. If none are present,
            the pathing query is skipped. Defaults to True.
        danger_distance: If `sense_danger` is True, how far to check for dangers.
            Defaults to 20.0.
        danger_threshold: Influence at which a danger is respected.
            Defaults to 5.0.

    """

    unit: Unit
    grid: np.ndarray
    target: Point2
    success_at_distance: float = 0.0
    sensitivity: int = 5
    smoothing: bool = False
    sense_danger: bool = True
    danger_distance: float = 20.0
    danger_threshold: float = 5.0

    def execute(self, ai: "AresBot", config: dict, mediator: ManagerMediator) -> bool:
        distance_to_target: float = cy_distance_to(self.unit.position, self.target)
        # no action executed
        if distance_to_target < self.success_at_distance:
            return False

        move_to: Point2 = mediator.find_path_next_point(
            start=self.unit.position,
            target=self.target,
            grid=self.grid,
            sensitivity=self.sensitivity,
            smoothing=self.smoothing,
            sense_danger=self.sense_danger,
            danger_distance=self.danger_distance,
            danger_threshold=self.danger_threshold,
        )
        self.unit.move(move_to)
        return True
