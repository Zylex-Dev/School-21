#include "grep.h"

int process_file(const char *file_name, const grep_flags *flags) {
  FILE *file;
  if (open_file_for_reading(file_name, &file, flags) == -1) {
    return EXIT_FAILURE;
  }

  char buffer[MAX_BUFFER_SIZE];
  int local_match_count = 0;  // -c
  int file_has_match = 0;     // -l
  int line_number = 0;

  while (fgets(buffer, sizeof(buffer), file) != NULL) {
    line_number++;

    int matches = process_patterns(buffer, line_number, file_name, flags);

    if (flags->c_flag) {
      local_match_count += matches;
    }

    if (flags->l_flag && matches > 0) {
      file_has_match = 1;
      break;
    }
  }

  fclose(file);

  if (flags->c_flag) {
    printf("%d\n", local_match_count);
  }

  if (flags->l_flag && file_has_match) {
    printf("%s\n", file_name);
  }

  return EXIT_SUCCESS;
}

int process_patterns(const char *line, int line_number, const char *file_name,
                     const grep_flags *flags) {
  int matches = 0;

  if (flags->f_file) {
    matches = process_with_pattern_file(line, flags);
  } else {
    matches = process_with_inline_patterns(line, flags);
  }

  if (flags->v_flag) {
    matches = !matches;
  }

  if (matches && !flags->c_flag && !flags->l_flag && !flags->o_flag) {
    print_line(line, line_number, file_name, flags);
  }

  return matches;
}

int process_with_pattern_file(const char *line, const grep_flags *flags) {
  FILE *pattern_file;
  if (open_file_for_reading(flags->f_file, &pattern_file, flags) == -1) {
    return -1;
  }

  char pattern_buffer[MAX_BUFFER_SIZE];
  int matches = 0;

  while (fgets(pattern_buffer, sizeof(pattern_buffer), pattern_file) != NULL) {
    pattern_buffer[strcspn(pattern_buffer, "\n")] =
        '\0';  // Удаление символа новой строки

    int match_found = match_pattern(line, pattern_buffer, flags);

    if (match_found) {
      matches = 1;
      break;
    }
  }

  fclose(pattern_file);
  return matches;
}

int process_with_inline_patterns(const char *line, const grep_flags *flags) {
  int matches = 0;
  for (int i = 0; i < flags->pattern_count; i++) {
    int match_found = match_pattern(line, flags->patterns[i], flags);

    if (match_found) {
      matches = 1;
      break;
    }
  }

  return matches;
}