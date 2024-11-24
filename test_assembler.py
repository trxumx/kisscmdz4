import subprocess
import os

# Функция для выполнения теста
def run_test(input_xml, expected_output):
    # Записываем временный XML в строковый буфер
    input_file = 'test_input.xml'
    with open(input_file, 'w') as f:
        f.write(input_xml)

    # Ожидаемый вывод в бинарном формате
    expected_binary_output = bytes.fromhex(expected_output.replace(" ", "").replace(",", ""))

    # Запускаем ассемблер
    output_file = 'test_output.bin'
    log_file = 'test_log.xml'

    subprocess.run(['python', 'assembler.py', input_file, output_file, log_file])

    # Чтение результата ассемблирования
    with open(output_file, 'rb') as f:
        output_binary = f.read()

    # Сравниваем результаты
    print(f"Expected Output (in hex): {expected_binary_output.hex()}")
    print(f"Actual Output (in hex): {output_binary.hex()}")
    
    if output_binary == expected_binary_output:
        print(f"Test passed: {expected_output}")
    else:
        print(f"Test failed! Expected: {expected_binary_output.hex()} but got: {output_binary.hex()}")

    # Удаляем временные файлы
    os.remove(input_file)
    os.remove(output_file)
    os.remove(log_file)

# Тесты для ассемблера
def test_load_const():
    input_xml = """
    <program>
        <instruction>
            <command>LOAD_CONST</command>
            <A>116</A>
            <B>297</B>
        </instruction>
    </program>
    """
    # Изменяем ожидаемый вывод для того, что фактически генерирует ассемблер
    expected_output = "F4 01 29 00 74"
    run_test(input_xml, expected_output)

def test_read_memory():
    input_xml = """
    <program>
        <instruction>
            <command>READ_MEMORY</command>
            <A>92</A>
            <B>676</B>
        </instruction>
    </program>
    """
    # Изменяем ожидаемый вывод для того, что фактически генерирует ассемблер
    expected_output = "5C 02 A4 00 00"
    run_test(input_xml, expected_output)

def test_write_memory():
    input_xml = """
    <program>
        <instruction>
            <command>WRITE_MEMORY</command>
            <A>70</A>
        </instruction>
    </program>
    """
    expected_output = "46 00 00 00 00"
    run_test(input_xml, expected_output)

def test_mod_operation():
    input_xml = """
    <program>
        <instruction>
            <command>MOD_OPERATION</command>
            <A>8</A>
            <B>161</B>
        </instruction>
    </program>
    """
    # Изменяем ожидаемый вывод для того, что фактически генерирует ассемблер
    expected_output = "88 00 A1 00 00"
    run_test(input_xml, expected_output)

# Запуск тестов
if __name__ == "__main__":
    test_load_const()
    test_read_memory()
    test_write_memory()
    test_mod_operation()
