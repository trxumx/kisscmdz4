import subprocess
import os
import unittest


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

    # Проверка результатов
    assert output_binary == expected_binary_output, f"Test failed! Expected: {expected_binary_output.hex()} but got: {output_binary.hex()}"

    # Удаляем временные файлы
    os.remove(input_file)
    os.remove(output_file)
    os.remove(log_file)


# Класс тестов для ассемблера
class TestAssembler(unittest.TestCase):

    def test_mod_operation(self):
        input_xml = """
        <program>
            <instruction>
                <command>MOD_OPERATION</command>
                <A>5</A>
                <B>3</B>
                <index>0</index>
            </instruction>
            <instruction>
                <command>MOD_OPERATION</command>
                <A>10</A>
                <B>3</B>
                <index>1</index>
            </instruction>
            <instruction>
                <command>MOD_OPERATION</command>
                <A>20</A>
                <B>7</B>
                <index>2</index>
            </instruction>
            <instruction>
                <command>MOD_OPERATION</command>
                <A>50</A>
                <B>9</B>
                <index>3</index>
            </instruction>
        </program>
        """
        # Ожидаемый вывод в бинарном формате, который генерирует ассемблер
        expected_output = "88 00 03 00 00 88 00 03 00 00 88 00 07 00 00 88 00 09 00 00"
        run_test(input_xml, expected_output)

    def tearDown(self):
        # Очистка временных файлов после каждого теста
        if os.path.exists('test_input.xml'):
            os.remove('test_input.xml')
        if os.path.exists('test_output.bin'):
            os.remove('test_output.bin')
        if os.path.exists('test_log.xml'):
            os.remove('test_log.xml')


# Запуск тестов
if __name__ == "__main__":
    unittest.main()
