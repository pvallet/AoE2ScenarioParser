from src.helper.retriever import find_retriever
from src.objects.data_header_obj import DataHeaderObject
from src.objects.diplomacy_obj import DiplomacyObject
from src.objects.file_header_obj import FileHeaderObject
from src.objects.messages_obj import MessagesObject
from src.objects.options_obj import OptionsObject
from src.objects.player_object import PlayerObject
import src.helper.generator as generator


class AoE2ObjectManager:
    def __init__(self, parser_header, parsed_data):
        self.parser_header = parser_header
        self.parsed_data = parsed_data
        self.objects = {}

        print("\n"*16)
        self.objects["FileHeaderObject"] = self._parse_file_header_object()
        self.objects["DataHeaderObject"] = self._parse_data_header_object()
        self.objects["PlayerObject"] = self._parse_player_object()
        self.objects["MessagesObject"] = self._parse_messages_object()
        self.objects["DiplomacyObject"] = self._parse_diplomacy_object()
        self.objects["OptionsObject"] = self._parse_options_object()
        print("\n"*16, self.objects)

    def _parse_options_object(self):
        object_piece = self.parsed_data['OptionsPiece']
        # ppnd: Per Player Number of Disabled
        ppnd_techs = find_retriever(object_piece.retrievers, "Per player number of disabled techs").data
        ppnd_units = find_retriever(object_piece.retrievers, "Per player number of disabled units").data
        ppnd_buildings = find_retriever(object_piece.retrievers, "Per player number of disabled buildings").data
        disabled_techs = generator.create_generator(
            find_retriever(object_piece.retrievers, "Disabled technology IDs in player order").data, 1
        )
        disabled_units = generator.create_generator(
            find_retriever(object_piece.retrievers, "Disabled unit IDs in player order").data, 1
        )
        disabled_buildings = generator.create_generator(
            find_retriever(object_piece.retrievers, "Disabled building IDs in player order").data, 1
        )

        disables = list()
        for player_id in range(0, 8):  # 0-7 Players
            nd_techs = ppnd_techs[player_id]
            nd_units = ppnd_units[player_id]
            nd_buildings = ppnd_buildings[player_id]
            player_disabled_techs = generator.repeat_generator(
                disabled_techs, nd_techs, return_bytes=False)
            player_disabled_units = generator.repeat_generator(
                disabled_units, nd_units, return_bytes=False)
            player_disabled_buildings = generator.repeat_generator(
                disabled_buildings, nd_buildings, return_bytes=False)

            disables.append({
                'techs': player_disabled_techs,
                'units': player_disabled_units,
                'buildings': player_disabled_buildings,
            })

        return OptionsObject(
            disables,
            find_retriever(object_piece.retrievers, "All techs").data
        )

    def _parse_diplomacy_object(self):
        diplomacies = []

        object_piece = self.parsed_data['DiplomacyPiece']
        diplomacy = find_retriever(object_piece.retrievers, "Per-player diplomacy").data

        for player_id in range(0, 8):  # 0-7 Players
            diplomacies.append(DiplomacyObject(
                player_number=player_id,
                stance_per_player=find_retriever(diplomacy[player_id].retrievers, "Stance with each player").data
            ))

        return diplomacies

    def _parse_messages_object(self):
        object_piece = self.parsed_data['MessagesPiece']
        retrievers = object_piece.retrievers

        new_object = MessagesObject(
            instructions=find_retriever(retrievers, "Instructions").data,
            hints=find_retriever(retrievers, "Hints").data,
            victory=find_retriever(retrievers, "Victory").data,
            loss=find_retriever(retrievers, "Loss").data,
            history=find_retriever(retrievers, "History").data,
            scouts=find_retriever(retrievers, "Scouts").data,
            ascii_instructions=find_retriever(retrievers, "ASCII Instructions").data,
            ascii_hints=find_retriever(retrievers, "ASCII Hints").data,
            ascii_victory=find_retriever(retrievers, "ASCII Victory").data,
            ascii_loss=find_retriever(retrievers, "ASCII Loss").data,
            ascii_history=find_retriever(retrievers, "ASCII History").data,
            ascii_scouts=find_retriever(retrievers, "ASCII Scouts").data,
        )
        return new_object

    def _parse_player_object(self):
        players = []

        data_header_piece = self.parsed_data['DataHeaderPiece']
        unit_piece = self.parsed_data['UnitsPiece']
        options_piece = self.parsed_data['OptionsPiece']
        starting_ages = find_retriever(options_piece.retrievers, "Per player starting age").data

        # Player Data
        player_data_one = find_retriever(data_header_piece.retrievers, "Player data#1").data  # 0-7 Players & 8 Gaia
        player_data_two = self.parsed_data['PlayerDataTwoPiece']  # 0-7 Players & 8 Gaia
        resources = find_retriever(player_data_two.retrievers, "Resources").data
        player_data_three = find_retriever(unit_piece.retrievers, "Player data #3").data  # 0-7 Players
        player_data_four = find_retriever(unit_piece.retrievers, "Player data #4").data  # 0-7 Players

        for player_id in range(0, 9):  # 0-7 Players & 8 Gaia:
            try:  # If gaia isn't saved. (PlayerDataThree and PlayerDataFour)
                pop_limit = find_retriever(player_data_four[player_id].retrievers, "Population limit").data
            except IndexError as e:
                pop_limit = -1

            players.append(PlayerObject(
                player_number=player_id,
                active=find_retriever(player_data_one[player_id].retrievers, "Active").data,
                human=find_retriever(player_data_one[player_id].retrievers, "Human").data,
                civilization=find_retriever(player_data_one[player_id].retrievers, "Civilization").data,
                gold=find_retriever(resources[player_id].retrievers, "Gold").data,
                wood=find_retriever(resources[player_id].retrievers, "Wood").data,
                food=find_retriever(resources[player_id].retrievers, "Food").data,
                stone=find_retriever(resources[player_id].retrievers, "Stone").data,
                color=find_retriever(resources[player_id].retrievers, "Player color").data,
                starting_age=starting_ages[player_id],
                pop_limit=pop_limit
            ))

        return players

    def _parse_data_header_object(self):
        object_piece = self.parsed_data['DataHeaderPiece']
        retrievers = object_piece.retrievers

        new_object = DataHeaderObject(
            version=find_retriever(retrievers, "Version").data,
            filename=find_retriever(retrievers, "Filename").data
        )
        return new_object

    def _parse_file_header_object(self):
        object_piece = self.parser_header['FileHeaderPiece']
        retrievers = object_piece.retrievers

        new_object = FileHeaderObject(
            version=find_retriever(retrievers, "Version").data,
            timestamp=find_retriever(retrievers, "Timestamp of last save").data,
            instructions=find_retriever(retrievers, "Scenario instructions").data,
            player_count=find_retriever(retrievers, "Player count").data,
            creator_name=find_retriever(retrievers, "Creator name").data,
        )
        return new_object