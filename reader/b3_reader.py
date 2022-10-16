import re
from typing import Dict, List


def is_inside_rect(rect: List[float], boundary_rect: List[float]) -> bool:
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = rect

    boundary_top_left_x, boundary_top_left_y, boundary_bottom_right_x, boundary_bottom_right_y = boundary_rect

    is_out = False

    if top_left_x < boundary_top_left_x:
        is_out = True
    elif top_left_y < boundary_top_left_y:
        is_out = True
    elif bottom_right_x > boundary_bottom_right_x:
        is_out = True
    elif bottom_right_y > boundary_bottom_right_y:
        is_out = True

    return not is_out


def is_inside_line(line: List[float], boundary_line: List[float]):
    left, right = line

    boundary_left, boundary_right = boundary_line

    return left > boundary_left and right < boundary_right


class B3Reader:
    raw_content = []

    info_areas_setting = {}
    negotiations_columns_settings = {}

    mapped_content = {
        "info": {},
        "negotiations": []
    }

    def __init__(self, page, settings):
        self.info_areas_setting = settings.get("info_areas")
        self.negotiations_columns_settings = settings.get(
            "negotiations_columns")

        self.page = page

        self.raw_content = self.get_raw_content(page)

    def get_raw_content(self, page):
        return page.get_text("words", sort=True)

    def get_mapped_content(self):
        return self.__map_page_content()

    def __map_page_content(self):
        mapped_negotiations = {}
        mapped_info = {}
        for content in self.raw_content:
            area_name = self.__get_area_name(content)

            if area_name:
                self.__save_info_content_in(
                    mapped_info, area_name, content[4])

            else:
                column_name = self.__get_column_name(content)

                if column_name:
                    self.__save_negotiation_in(
                        mapped_negotiations, content[1], column_name, content[4])

        self.mapped_content["negotiations"] = self.__parse_negotiations(
            mapped_negotiations)
        self.mapped_content["info"] = self.__parse_infos(mapped_info)

        return self.mapped_content

    def __get_area_name(self, word):
        boundaries = self.info_areas_setting

        for area_name, area_boundary in boundaries.items():
            boundary_rect = area_boundary["top_left"] + \
                area_boundary["bottom_right"]

            if is_inside_rect(word[:4], boundary_rect):
                return area_name

        return None

    def __get_column_name(self, content):
        boundaries = self.negotiations_columns_settings

        for column_name, column_boundary in boundaries.items():

            boundary_line = [column_boundary["left"], column_boundary["right"]]

            if (is_inside_line([content[0], content[2]], boundary_line)):
                return column_name

        return None

    def __save_content_in(self, obj: Dict, key: str, content: str):
        if (obj.get(key)):
            obj[key].append(content)
        else:
            obj[key] = [content]

    def __save_info_content_in(self, obj: Dict, key, content):
        self.__save_content_in(obj, key, content)

    def __save_negotiation_in(self, obj: Dict, key: str, column_name,  content: str):
        if (obj.get(key)):
            self.__save_content_in(obj[key], column_name, content)
        else:
            obj[key] = {
                column_name: [content]
            }

    def __parse_negotiations(self, negotiations):
        negotiations_array = []

        for negotiation in negotiations.values():
            if self.__is_negotiation(negotiation):
                parsed_negotiation = self.__parse_negotiation(negotiation)

                negotiations_array.append(parsed_negotiation)

        return negotiations_array

    def __parse_negotiation(self, negotiation):
        parsed_negotiation = {}

        for key, column in negotiation.items():
            parsed_negotiation[key] = " ".join(column)

        return parsed_negotiation

    def __parse_infos(self, infos):
        parsed_infos = {}
        settings = self.info_areas_setting

        for key, info in infos.items():
            info_settings = settings.get(key)

            parsed_infos[key] = self.__parse_info(info, info_settings)

        return parsed_infos

    def __parse_info(self, info, settings):
        initial_index = settings.get("initial_index")
        regex = settings.get("regex")

        if (initial_index is not None):
            return " ".join(info[initial_index:])
        elif (isinstance(regex, dict)):
            string = " ".join(info)
            results = {}

            for key, value in regex.items():
                teste = re.search(value, string)

                if (teste):
                    results[key] = teste.group()

            return results
        elif (regex is not None):
            return " ".join(info)

        return info

    def __is_negotiation(self, negotiation):
        items = negotiation.values()

        column_q = negotiation.get("q")

        if (column_q and column_q[0] in "qQ"):
            return False

        if len(items) >= 7:
            return True

        return False
