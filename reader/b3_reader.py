
from typing import Any, Dict, List


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


def save_word(dict: Dict, key: str, word: str):
    if (dict.get(key)):
        dict[key].append(word)
    else:
        dict[key] = [word]


def save_negotiation(dict: Dict, key: str, column_name,  word: str):
    if (dict.get(key)):
        save_word(dict[key], column_name, word)
    else:
        dict[key] = {
            column_name: [word]
        }


def get_raw_words(page):
    return page.get_text("words", sort=True)


def extract_mapped_words(page: Any, settings: Any):
    words = get_raw_words(page)

    mapped_words = map_words(words, settings)

    return mapped_words


def get_mapped_area(word, boundaries):
    mapped_areas = {}

    is_found = False

    for area_name, area_boundary in boundaries.items():
        boundary_rect = area_boundary["top_left"] + \
            area_boundary["bottom_right"]

        is_found = is_inside_rect(word[:4], boundary_rect)

        if is_found:
            save_word(mapped_areas, area_name, word[4])
            break

    return (mapped_areas, is_found)


def get_area_name(word, boundaries):
    for area_name, area_boundary in boundaries.items():
        boundary_rect = area_boundary["top_left"] + \
            area_boundary["bottom_right"]

        if is_inside_rect(word[:4], boundary_rect):
            return area_name


def get_column_name(word, boundaries):
    for column_name, column_boundary in boundaries.items():

        boundary_line = [column_boundary["left"], column_boundary["right"]]

        if (is_inside_line([word[0], word[2]], boundary_line)):
            return column_name


def map_words(words, boundaries):
    mapped_words = {}

    area_boundaries = boundaries["mapped_areas"]

    negotiation_column_boundaries = boundaries["negotiations_columns"]

    mapped_words["info"] = {}
    mapped_words["negotiations"] = {}

    for word in words:
        area_name = get_area_name(word, area_boundaries)

        if area_name:
            save_word(mapped_words["info"], area_name, word[4])

        else:
            column_name = get_column_name(word, negotiation_column_boundaries)

            if column_name:
                save_negotiation(
                    mapped_words["negotiations"], word[1], column_name, word[4])

                break

    return mapped_words


class B3Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse_broker(self):
        pass

    def parse_client(self):
        pass

    def parse_negotiations(self):
        pass
