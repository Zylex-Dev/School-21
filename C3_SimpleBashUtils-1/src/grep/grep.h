#ifndef GREP_H
#define GREP_H

#include <getopt.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_BUFFER_SIZE 1024
#define MAX_FILES 100

typedef struct {
  int e_flag;  // Шаблон из аргументов
  int i_flag;  // Игнорирование регистра
  int v_flag;  // Инверсия поиска
  int c_flag;  // Подсчет строк
  int l_flag;  // Вывод только имен файлов
  int n_flag;  // Номера строк
  int h_flag;  // Отключение имен файлов в выводе
  int s_flag;  // Подавление ошибок
  int f_flag;  // Шаблоны из файла
  int o_flag;  // Вывод совпавших частей строки
  char **patterns;              // Шаблоны
  int pattern_count;            // Количество шаблонов
  char *file_names[MAX_FILES];  // хранение имен файлов
  int file_count;               // Количество файлов
  char *f_file;                 // Имя файла для флага -f
  int match_count;  // Количество строк, которые соответствуют шаблону (для
                    // флага -c)
} grep_flags;

int flags_parser(int argc, char *argv[], grep_flags *flags);
void cleanup_grep_flags(grep_flags *flags);
int open_file_for_reading(const char *file_name, FILE **file,
                          const grep_flags *flags);
int process_file(const char *file_name, const grep_flags *flags);
int process_patterns(const char *line, int line_number, const char *file_name,
                     const grep_flags *flags);
int process_with_pattern_file(const char *line, const grep_flags *flags);
int process_with_inline_patterns(const char *line, const grep_flags *flags);
void print_line(const char *line, int line_number, const char *file_name,
                const grep_flags *flags);
int match_pattern(const char *line, const char *pattern,
                  const grep_flags *flags);
int main(int argc, char *argv[]);

#endif  // GREP_H
