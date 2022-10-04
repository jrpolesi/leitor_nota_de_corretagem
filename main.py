import json
import fitz

from reader.b3_reader import B3Reader


def main():
    doc = fitz.open("example.pdf")
    settings_file = open("setting.json")

    settings = json.load(settings_file)

    settings_file.close()

    reader = B3Reader(doc[0], settings)
    test = reader.get_mapped_content()

    print(json.dumps(test, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
