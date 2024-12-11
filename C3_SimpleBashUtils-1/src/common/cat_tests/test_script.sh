#!/bin/bash

# Убедитесь, что исполняемый файл s21_cat существует
if ! [ -f "./s21_cat" ]; then
    echo "Executable file ./s21_cat not found!"
    exit 1
fi

# Исходные файлы для тестирования
FILES=("../common/cat_tests/test_file.txt")  # Множество файлов для тестирования

# Проверка существования файлов
for FILE in "${FILES[@]}"; do
    if ! [ -f "$FILE" ]; then
        echo "File $FILE not found!"
        exit 1
    fi
done

# Список флагов для утилиты cat (включая GNU эквиваленты)
FLAGS=(
    "-b" "--number-nonblank"   # Нумерация только непустых строк
    "-e" "-E"                  # Показывает символы конца строки как $ и включает -v (для -E без -v)
    "-n" "--number"            # Нумерация всех строк
    "-s" "--squeeze-blank"     # Сжатие нескольких смежных пустых строк
    "-t" "-T"                  # Показывает табуляции как ^I и включает -v (для -T без -v)
)

# Проход по каждому флагу
for FLAG in "${FLAGS[@]}"; do
    echo "Testing flag $FLAG..."

    for FILE in "${FILES[@]}"; do
        # Проверяем, что файл существует
        if [ -f "$FILE" ]; then
            # Запуск cat и s21_cat для флагов
            ../cat/s21_cat $FLAG "$FILE" > s21_output.txt
            cat $FLAG "$FILE" > cat_output.txt

            # Сравнение выводов с помощью diff
            if diff -q s21_output.txt cat_output.txt > /dev/null; then
                echo "Flag $FLAG for file $FILE: ✅ Match"
            else
                echo "Flag $FLAG for file $FILE: ❌ Differences"
                echo "Differences:"
                diff s21_output.txt cat_output.txt
            fi
        else
            echo "File $FILE not found, skipping..."
        fi
    done
done

# Удаление временных файлов
rm -f s21_output.txt cat_output.txt