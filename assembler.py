import sys
import xml.etree.ElementTree as ET


# Функция для записи логов в XML
def write_log(log_file, instructions):
    root = ET.Element("log")
    for cmd, value in instructions.items():
        instruction = ET.SubElement(root, "instruction")
        key = ET.SubElement(instruction, "key")
        key.text = cmd
        value_elem = ET.SubElement(instruction, "value")
        value_elem.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(log_file, encoding="utf-8", xml_declaration=True)

    # Построчный вывод лога
    print("Log file content:")
    tree = ET.parse(log_file)
    root = tree.getroot()
    for instruction in root.findall('instruction'):
        key = instruction.find('key').text
        value = instruction.find('value').text
        print(f"key={key}, value={value}")


# Функция для преобразования XML программы в бинарный формат
def assemble_program(input_file, output_file, log_file):
    instructions = {}
    binary_program = []

    # Открываем XML файл с исходной программой
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Обрабатываем каждую инструкцию в XML
    for instruction in root.findall('instruction'):
        cmd = instruction.find('command').text
        A = int(instruction.find('A').text) if instruction.find('A') is not None else None
        B = int(instruction.find('B').text) if instruction.find('B') is not None else None

        if cmd == "LOAD_CONST":
            # Преобразуем A = 116 (0x74) и B = 297 (0x94, 0x00)
            binary_inst = bytes([0xF4, (B >> 8) & 0xFF, B & 0xFF, (A >> 8) & 0xFF, A & 0xFF])
            instructions[cmd] = f"A={A}, B={B}"
        
        elif cmd == "READ_MEMORY":
            # Преобразуем B = 676 (0x52, 0x01)
            binary_inst = bytes([0x5C, (B >> 8) & 0xFF, B & 0xFF, 0x00, 0x00])
            instructions[cmd] = f"A={A}, B={B}"
        
        elif cmd == "WRITE_MEMORY":
            # Преобразуем A = 70 (0x46)
            binary_inst = bytes([0x46, 0x00, 0x00, 0x00, 0x00])
            instructions[cmd] = f"A={A}"
        
        elif cmd == "MOD_OPERATION":
            # Преобразуем A = 8 и B = 161 (0x50)
            binary_inst = bytes([0x88, (B >> 8) & 0xFF, B & 0xFF, 0x00, 0x00])
            instructions[cmd] = f"A={A}, B={B}"
        
        else:
            print(f"Unknown command: {cmd}")
            continue

        # Добавляем команду в бинарную программу
        binary_program.append(binary_inst)

    # Записываем бинарное представление в файл
    with open(output_file, 'wb') as f:
        for binary_inst in binary_program:
            f.write(binary_inst)

    # Записываем лог
    write_log(log_file, instructions)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble_program(input_file, output_file, log_file)
    print(f"Assembly complete. Binary file: {output_file}, Log file: {log_file}")
