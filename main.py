import json
import fitz

from reader.b3_reader import extract_mapped_words

def main():
    doc = fitz.open("example.pdf")
    setting = open("setting.json")

    test = extract_mapped_words(doc[0], json.load(setting))

    print(json.dumps(test, sort_keys=True, indent=4))

    setting.close()


if __name__ == '__main__':
    main()
