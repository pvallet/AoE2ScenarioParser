from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
from AoE2ScenarioParser.pieces.structs.aoe2_struct import AoE2Struct


class VariableStruct(AoE2Struct):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("variable_id", DataType("u32")),
            Retriever("name", DataType("str32")),
        ]

        super().__init__("Variable", retrievers, parser_obj, data)
