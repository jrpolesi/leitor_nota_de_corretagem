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
        "negotiations": {}
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
        for content in self.raw_content:
            area_name = self.__get_area_name(content)

            if area_name:
                self.__save_info_content(area_name, content[4])

            else:
                column_name = self.__get_column_name(content)

                if column_name:
                    self.__save_negotiation(
                        content[1], column_name, content[4])

        self.__name_negotiations_rows()

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

    def __save_info_content(self, key, content):
        info_contents = self.mapped_content["info"]

        self.__save_content_in(info_contents, key, content)

    def __save_negotiation(self, key: str, column_name,  content: str):
        negotiations = self.mapped_content["negotiations"]

        if (negotiations.get(key)):
            self.__save_content_in(negotiations[key], column_name, content)
        else:
            negotiations[key] = {
                column_name: [content]
            }

    def __name_negotiations_rows(self):
        negotiations = self.mapped_content["negotiations"]
        named_negotiations = {}

        for key, row in negotiations.items():
            new_name = row.get("column_especificacao_do_titulo")

            if (new_name and self.__is_negotiation(row)):
                named_negotiations["_".join(new_name)] = negotiations.get(key)

        self.mapped_content["negotiations"] = named_negotiations

    def __is_negotiation(self, negotiation):
        items = negotiation.values()

        column_q = negotiation.get("column_q")

        if (column_q and column_q[0] in "qQ"):
            return False

        if len(items) >= 7:
            return True

        return False
