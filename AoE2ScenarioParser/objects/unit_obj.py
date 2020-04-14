from __future__ import annotations

from AoE2ScenarioParser.helper.retriever import find_retriever
from AoE2ScenarioParser.objects.aoe2_object import AoE2Object
from AoE2ScenarioParser.pieces.structs.unit import UnitStruct


class UnitObject(AoE2Object):
    def __init__(self,
                 player,
                 x,
                 y,
                 z,
                 reference_id,
                 unit_id,
                 status,
                 rotation,
                 animation_frame,
                 garrisoned_in_id
                 ):

        self._player = player
        """
        PLEASE NOTE: This is an internal (read-only) value for ease of access. It DOES NOT represent the actual player 
        controlling the unit. To change which player controls this unit, use:
            unit_manager.change_ownership(UnitObject, to_player[, from_player, skip_gaia])
        """
        self.x = x
        self.y = y
        self.z = z
        self.reference_id = reference_id
        self.unit_id = unit_id
        self.status = status
        self.rotation = rotation
        self.animation_frame = animation_frame
        self.garrisoned_in_id = garrisoned_in_id

        super().__init__()

    @property
    def player(self):
        return self._player

    @staticmethod
    def _parse_object(parsed_data, **kwargs) -> UnitObject:  # Expected {unit=unitStruct, player=Player}
        unit = kwargs['unit']

        return UnitObject(
            player=kwargs['player'],
            x=find_retriever(unit.retrievers, "X position").data,
            y=find_retriever(unit.retrievers, "Y position").data,
            z=find_retriever(unit.retrievers, "Z position").data,
            reference_id=find_retriever(unit.retrievers, "ID").data,
            unit_id=find_retriever(unit.retrievers, "Unit 'constant'").data,
            status=find_retriever(unit.retrievers, "Status").data,
            rotation=find_retriever(unit.retrievers, "Rotation, in radians").data,
            animation_frame=find_retriever(unit.retrievers, "Initial animation frame").data,
            garrisoned_in_id=find_retriever(unit.retrievers, "Garrisoned in: ID").data,
        )

    @staticmethod
    def _reconstruct_object(parsed_data, objects, **kwargs) -> None:  # Expected {unit=unit_obj, units=units_list}
        unit_obj = kwargs['unit']
        units_list = kwargs['units']

        data_list = [value for key, value in vars(unit_obj).items()]
        del data_list[0]  # Remove player attribute

        units_list.append(UnitStruct(data=data_list))
