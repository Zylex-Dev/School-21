#ifndef S21_CAT_H
#define S21_CAT_H

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define _POSIX_C_SOURCE 201709L
#define BUFFER_SIZE 1024

extern char *optarg;
extern int optind, opterr, optopt;

int is_file_exist(const char *fname);
void copy_file_to_temp(const char *source_file, FILE *temp_file);
void print_temp_file(FILE *temp_file);
void process_file(FILE *temp_file, void (*process_line)(const char *, FILE *));
void process_line_n(const char *line, FILE *output);
void process_line_b(const char *line, FILE *output);
void process_line_t(const char *line, FILE *output);
void process_line_v(const char *line, FILE *output);
void process_line_e(const char *line, FILE *output);
void process_line_s(const char *line, FILE *output);
void v_flag_realization(FILE *temp_file);
void t_flag_realization(FILE *temp_file);
void s_flag_realization(FILE *temp_file);
void n_flag_realization(FILE *temp_file);
void b_flag_realization(FILE *temp_file);
void e_flag_realization(FILE *temp_file);
void process_file_with_flags(char const *source_file, int flag_b, int flag_e,
                             int flag_n, int flag_s, int flag_t, int flag_v,
                             int flag_E, int flag_T);
int main(int argc, char **argv);

#endif
