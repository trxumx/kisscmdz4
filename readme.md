Домашнее задание №4 - Ассемблер и интерпретатор УВМ

Запуск ассемблера:
```bash
python assembler.py test_input.xml test_output.bin test_log.xml
```

Запуск интерпретатора:
```bash
python interpreter.py test_output.bin result.xml 0 100
```

Запуск тестов ассемблера с покрытием:
```bash
coverage run --source=test_assembler -m test_assembler
```

Запуск тестовой программы (взятия остатков от вектора) с покрытием:
```bash
coverage run --source=test_mod_operation -m test_mod_operation 
```