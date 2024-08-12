import os
import json

def count_characters_in_json_files(folder_path):
    # Obtener la ruta absoluta al script
    script_path = os.path.abspath(__file__)
    # Obtener el directorio del script
    script_dir = os.path.dirname(script_path)
    # Obtener la ruta absoluta a la carpeta
    full_path = os.path.join(script_dir, folder_path)

    # Verificar si la carpeta existe
    if not os.path.isdir(full_path):
        print(f"La carpeta '{full_path}' no existe.")
        return 0

    print(f"Contando caracteres en archivos JSON en: {full_path}")

    total_characters = 0
    for filename in os.listdir(full_path):
        if filename.endswith(".json"):
            file_path = os.path.join(full_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    char_count = len(content)
                    total_characters += char_count
                    print(f"Archivo '{filename}' tiene {char_count} caracteres.")
            except FileNotFoundError:
                print(f"Archivo '{file_path}' no encontrado.")
            except IOError as e:
                print(f"Error al abrir el archivo '{file_path}': {e}")

    print(f"Total de caracteres en la carpeta '{folder_path}': {total_characters}\n")
    return total_characters

def calculate_tokens(char_count):
    words_count = char_count / 5  # Asumimos que 1 palabra = 5 caracteres en promedio
    tokens = (words_count / 750) * 1000  # 1000 tokens son aproximadamente 750 palabras
    return tokens

def main():
    paths_and_collections = {
        "JSON/InformacionPrivada/Q&A": "InformacionPrivada_QA",
        "JSON/InformacionPrivada/General": "InformacionPrivada_General",
        "JSON/InformacionPublica/Q&A": "InformacionPublica_QA",
        "JSON/InformacionPublica/General": "InformacionPublica_General"
    }

    total_characters_across_folders = 0

    for relative_path, _ in paths_and_collections.items():
        total_characters_in_folder = count_characters_in_json_files(relative_path)
        total_characters_across_folders += total_characters_in_folder

    print(f"Total de caracteres en todas las carpetas: {total_characters_across_folders}\n")

    total_tokens = calculate_tokens(total_characters_across_folders)
    print(f"Total de tokens estimados (Suponiendo que 1 palabra = 5 caracteres en promedio, y 1000 tokens = 750 palabras): {total_tokens:.2f}")

if __name__ == "__main__":
    main()
