import json
import os


def normalized_input(asking):
    return input(asking).strip()


def clear_terminal():
  user_operation_system = os.name

  if(user_operation_system == 'posix'):
      os.system("clear")
  else:
      os.system("cls")


def print_beauty_json(dict, indent=2):
    json_result = json.dumps(dict, indent=indent)

    print(json_result)


def to_rect(x, y, w, h):
    return {
        "top_left": [x, y],
        "bottom_right": [x + w, y + h]
    }


def ask_for_data():
    name = normalized_input("Digite um nome para area: ")

    x = float(normalized_input("Digite o eixo-x inicial: "))

    y = float(normalized_input("Digite o eixo-y inicial: "))

    width = float(normalized_input("Digite a largura: "))

    height = float(normalized_input("Digite a altura: "))

    return (name, x, y, width, height)


def main():
    formatted_rects = dict()

    try:
        while True:
            (name, x, y, width, height) = ask_for_data()

            mappedArea = to_rect(x, y, width, height)

            formatted_rects[name] = mappedArea

            shouldContinue = normalized_input("Deseja continuar? (Y/n) ")

            clear_terminal()
            
            if shouldContinue not in "yY":
                print_beauty_json(formatted_rects, indent=2)

                break
    except:
        print("Houve algum erro...")

        print_beauty_json(formatted_rects, indent=2)


main()
