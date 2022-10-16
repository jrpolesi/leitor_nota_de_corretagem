import json
import fitz

from reader.b3_reader import B3Reader


def main():
    doc = fitz.open("example.pdf")
    settings_file = open("setting.json", encoding="utf-8")

    settings = json.load(settings_file)

    settings_file.close()

    reader = B3Reader(doc[0], settings)
    mapped_content = reader.get_mapped_content()

    print(json.dumps(mapped_content, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
