#include "grep.h"

int open_file_for_reading(const char *file_name, FILE **file,
                          const grep_flags *flags) {
  *file = fopen(file_name, "r");
  if (*file == NULL) {
    if (!flags->s_flag) {
      fprintf(stderr, "grep: %s: No such file or directory\n", file_name);
    }
    return -1;
  }
  return EXIT_SUCCESS;
}

void cleanup_grep_flags(grep_flags *flags) {
  for (int i = 0; i < flags->pattern_count; i++) {
    free(flags->patterns[i]);
  }
  free(flags->patterns);
}