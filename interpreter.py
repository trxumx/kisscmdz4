import sys
import struct
import xml.etree.ElementTree as ET

# Функция для записи результатов в XML
def write_results(result_file, memory, start_addr, end_addr):
    root = ET.Element("result")
    for address, value in memory.items():
        # Сохраняем только те адреса, которые в указанном диапазоне
        if start_addr <= address <= end_addr:
            memory_elem = ET.SubElement(root, "memory")
            address_elem = ET.SubElement(memory_elem, "address")
            address_elem.text = str(address)
            value_elem = ET.SubElement(memory_elem, "value")
            value_elem.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(result_file, encoding="utf-8", xml_declaration=True)

    # Построчный вывод результата
    print("Result file content:")
    tree = ET.parse(result_file)
    root = tree.getroot()
    for memory_elem in root.findall('memory'):
        address = memory_elem.find('address').text
        value = memory_elem.find('value').text
        print(f"address={address}, value={value}")


# Интерпретатор команд УВМ
def interpret_program(input_file, result_file, start_addr, end_addr):
    memory = {}  # Эмулируем память
    stack = []   # Стек для операций
    pc = 0  # Программный счётчик

    # Открываем бинарный файл с программой
    with open(input_file, 'rb') as f:
        program = f.read()

    # Чтение и выполнение команд
    while pc < len(program):
        cmd = program[pc:pc + 5]
        if len(cmd) < 5:
            break  # Если команда неполная, выходим

        opcode = cmd[0]
        
        if opcode == 0xF4:  # LOAD_CONST
            A = (cmd[3] << 8) | cmd[4]
            B = (cmd[1] << 8) | cmd[2]
            stack.append(A)  # Добавляем A на стек
            memory[B] = A    # Записываем значение в память по адресу B
            print(f"LOAD_CONST: A={A}, B={B}")

        elif opcode == 0x5C:  # READ_MEMORY
            B = (cmd[1] << 8) | cmd[2]
            value = memory.get(B, 0)  # Чтение из памяти по адресу B
            stack.append(value)  # Добавляем в стек
            print(f"READ_MEMORY: Value at B={B} is {value}")

        elif opcode == 0x46:  # WRITE_MEMORY
            A = stack.pop()  # Снимаем значение с вершины стека
            memory[A] = A    # Записываем значение из стека в память
            print(f"WRITE_MEMORY: Writing value {A} to address {A}")

        elif opcode == 0x88:  # MOD_OPERATION
            B = (cmd[1] << 8) | cmd[2]
            A = stack.pop()  # Снимаем значение с вершины стека
            result = A % B
            memory[A] = result  # Результат операции записываем в память
            print(f"MOD_OPERATION: A={A}, B={B}, result={result}")

        else:
            print(f"Unknown opcode {opcode} at PC={pc}")

        pc += 5  # Переход к следующей команде

    # Записываем результаты в XML
    write_results(result_file, memory, start_addr, end_addr)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python interpreter.py <input_file> <result_file> <start_addr> <end_addr>")
        sys.exit(1)

    input_file = sys.argv[1]
    result_file = sys.argv[2]
    start_addr = int(sys.argv[3])
    end_addr = int(sys.argv[4])

    interpret_program(input_file, result_file, start_addr, end_addr)
    print(f"Interpretation complete. Result file: {result_file}")
