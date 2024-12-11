#!/bin/bash

# Убедитесь, что исполняемый файл s21_grep существует
if ! [ -f "./s21_grep" ]; then
    echo "Executable file ./s21_grep not found!"
    exit 1
fi

# Исходные файлы для тестирования
FILES=("../common/grep_tests/test_file.txt")  # Множество файлов для тестирования
PATTERN="lorem"          # Шаблон для поиска

# Файл с регулярными выражениями для флага -f
REGEX_FILE="../common/grep_tests/f_file.txt"

# Проверка существования файлов
for FILE in "${FILES[@]}"; do
    if ! [ -f "$FILE" ]; then
        echo "File $FILE not found!"
        exit 1
    fi
done

# Проверка существования файла с регулярными выражениями для флага -f
if ! [ -f "$REGEX_FILE" ]; then
    echo "File with regular expressions $REGEX_FILE not found!"
    exit 1
fi

# Список флагов
FLAGS=(
    "-e" "-i" "-v" "-c" "-l" "-n" "-s" "-f"
    "-o" "-in" "-iv" "-ic" "-il" "-vn" "-vc" "-vl"
)

# Проход по каждому флагу
for FLAG in "${FLAGS[@]}"; do
    echo "Testing flag $FLAG..."

    for FILE in "${FILES[@]}"; do
        # Проверяем, что файл существует
        if [ -f "$FILE" ]; then
            # Запуск grep и s21_grep для флага -f
            if [ "$FLAG" == "-f" ]; then
                ../grep/s21_grep $FLAG "$REGEX_FILE" "$FILE" > s21_output.txt
                grep $FLAG "$REGEX_FILE" "$FILE" > grep_output.txt
            else
                # Запуск для других флагов
                ../grep/s21_grep $FLAG "$PATTERN" "$FILE" > s21_output.txt
                grep $FLAG "$PATTERN" "$FILE" > grep_output.txt
            fi

            # Сравнение выводов с помощью diff
            if diff -q s21_output.txt grep_output.txt > /dev/null; then
                echo "Flag $FLAG for file $FILE: ✅ Match"
            else
                echo "Flag $FLAG for file $FILE: ❌ Differences"
                echo "Differences:"
                diff s21_output.txt grep_output.txt
            fi
        else
            echo "File $FILE not found, skipping..."
        fi
    done
done

# Удаление временных файлов
rm -f s21_output.txt grep_output.txt