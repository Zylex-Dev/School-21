#include "grep.h"

int match_pattern(const char *line, const char *pattern,
                  const grep_flags *flags) {
  regex_t regex;
  regmatch_t pmatch[1];  // To store the match position
  int result = 0;
  int gflags = REG_EXTENDED;

  if (flags->i_flag) {
    gflags |= REG_ICASE;
  }
  if (regcomp(&regex, pattern, gflags)) {
    return 0;
  }

  const char *search_start = line;
  while (regexec(&regex, search_start, 1, pmatch, 0) == 0) {
    if (flags->o_flag) {
      // prints the match substring
      int match_start = pmatch[0].rm_so;
      int match_end = pmatch[0].rm_eo;
      char match_text[MAX_BUFFER_SIZE];
      snprintf(match_text, match_end - match_start + 1, "%.*s",
               match_end - match_start, search_start + match_start);
      print_line(match_text, 0, NULL, flags);
    }
    result = 1;

    search_start +=
        pmatch[0].rm_eo;  // Moving the pointer to  find the next match
  }

  regfree(&regex);
  return result;
}