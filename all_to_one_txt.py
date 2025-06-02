import os
from pathlib import Path

def merge_code(source_dir: str, output_file: str, extensions: list = None):
    """
    Объединяет код из всех файлов в указанной директории
    :param source_dir: Путь к исходной папке
    :param output_file: Путь к выходному файлу
    :param extensions: Список разрешений файлов для включения (например ['.py', '.js'])
    """
    if extensions is None:
        extensions = ['.py', '.js', '.html', '.css', '.txt']
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            # Исключаем папку node_modules
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(f"\n\n{'='*50}\n")
                            outfile.write(f"FILE: {file_path}\n")
                            outfile.write(f"{'='*50}\n\n")
                            outfile.write(content)
                    except UnicodeDecodeError:
                        print(f"Skipping binary file: {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    # Настройки
    SOURCE_DIR = r"C:\Users\TECH - 103\Documents\new_gradebook"
    OUTPUT_FILE = "combined_code_front.txt"
    INCLUDE_EXTENSIONS = ['.py', '.js', '.jsx', '.html', '.css']
    
    merge_code(SOURCE_DIR, OUTPUT_FILE, INCLUDE_EXTENSIONS)
    print(f"All code merged into {OUTPUT_FILE}")
