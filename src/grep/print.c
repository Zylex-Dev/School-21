#include "grep.h"

void print_line(const char *line, int line_number, const char *file_name,
                const grep_flags *flags) {
  if (flags->o_flag) {
    printf("%s\n", line);
  } else {
    if (!flags->h_flag && flags->file_count > 1) {
      printf("%s:", file_name);
    }

    if (flags->n_flag) {
      printf("%d:", line_number);
    }

    printf("%s", line);

    // Add \n if it is not at the end of the line
    if (line[strlen(line) - 1] != '\n') {
      printf("\n");
    }
  }
}