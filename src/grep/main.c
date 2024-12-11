#include "grep.h"

int main(int argc, char *argv[]) {
  grep_flags flags = {0};
  int ret = flags_parser(argc, argv, &flags);
  if (ret != EXIT_SUCCESS) {
    return ret;
  }

  for (int i = 0; i < flags.file_count; i++) {
    int processing_status = (process_file(flags.file_names[i], &flags));
    if (processing_status != EXIT_SUCCESS) {
      return processing_status;
    }
  }

  cleanup_grep_flags(&flags);

  return 0;
}