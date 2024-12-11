#include "grep.h"

int flags_parser(int argc, char *argv[], grep_flags *flags) {
  int opt;
  opterr = 0;
  while ((opt = getopt(argc, argv, "e:ivclnhsf:o")) != -1) {
    switch (opt) {
      case 'e':
        flags->e_flag = 1;
        flags->patterns = realloc(flags->patterns,
                                  sizeof(char *) * (flags->pattern_count + 1));
        if (flags->patterns == NULL) {
          fprintf(stderr, "Error: Memory allocation failed for patterns.\n");
          return EXIT_FAILURE;
        }
        flags->patterns[flags->pattern_count] = strdup(optarg);
        if (flags->patterns[flags->pattern_count] == NULL) {
          fprintf(stderr,
                  "Error: Memory allocation failed for pattern string.\n");
          return EXIT_FAILURE;
        }
        flags->pattern_count++;
        break;
      case 'f':
        flags->f_flag = 1;
        flags->f_file = optarg;
        break;
      case 'i':
        flags->i_flag = 1;
        break;
      case 'v':
        flags->v_flag = 1;
        break;
      case 'c':
        flags->c_flag = 1;
        break;
      case 'l':
        flags->l_flag = 1;
        break;
      case 'n':
        flags->n_flag = 1;
        break;
      case 'h':
        flags->h_flag = 1;
        break;
      case 's':
        flags->s_flag = 1;
        break;
      case 'o':
        flags->o_flag = 1;
        break;
      default:
        fprintf(stderr,
                "Usage: ./grep [-e PATTERN] [-f FILE] [-ivclnhso] [FILE...]\n");
        return EXIT_FAILURE;
    }
  }

  for (int i = optind; i < argc; i++) {
    if (flags->pattern_count == 0 && !flags->f_flag) {
      // Если нет -e или -f, первый аргумент — это шаблон
      flags->patterns =
          realloc(flags->patterns, sizeof(char *) * (flags->pattern_count + 1));
      if (flags->patterns == NULL) {
        fprintf(stderr, "Error: Memory allocation failed for patterns.\n");
        return EXIT_FAILURE;
      }
      flags->patterns[flags->pattern_count] = strdup(argv[i]);
      if (flags->patterns[flags->pattern_count] == NULL) {
        fprintf(stderr,
                "Error: Memory allocation failed for pattern string.\n");
        return EXIT_FAILURE;
      }
      flags->pattern_count++;
    } else {
      // Остальные аргументы — это файлы
      if (flags->file_count < MAX_FILES) {
        flags->file_names[flags->file_count] = argv[i];
        flags->file_count++;
      } else {
        fprintf(stderr, "Error: Too many files specified.\n");
        return EXIT_FAILURE;
      }
    }
  }

  if (argc < 3) {
    fprintf(stderr,
            "Usage: ./grep [-e PATTERN] [-f FILE] [-ivclnhso] [FILE...]\n");
    return EXIT_FAILURE;
  }

  if (flags->e_flag && flags->pattern_count == 0) {
    fprintf(stderr, "Error: -e requires a pattern\n");
    return EXIT_FAILURE;
  }

  if (flags->f_flag) {
    if (!flags->f_file) {
      fprintf(stderr, "Error: -f requires a file name\n");
      return EXIT_FAILURE;
    }

    if (access(flags->f_file, R_OK) == -1) {
      fprintf(stderr, "Error: Cannot read file %s\n", flags->f_file);
      return EXIT_FAILURE;
    }

    // Проверка, что файл с шаблонами не пустой
    FILE *pattern_file = fopen(flags->f_file, "r");
    if (pattern_file) {
      int is_empty = (fgetc(pattern_file) == EOF);
      fclose(pattern_file);

      if (is_empty) {
        fprintf(stderr, "Error: Pattern file %s is empty\n", flags->f_file);
        return EXIT_FAILURE;
      }
    }
  }

  if (flags->c_flag && flags->l_flag) {
    // fprintf(stderr,
    //         "Warning: -c and -l are mutually exclusive. Ignoring -c.\n");
    flags->c_flag = 0;
  }

  if (flags->file_count == 0) {
    fprintf(stderr, "Error: file is required\n");
    return EXIT_FAILURE;
  }

  if (flags->file_count >= MAX_FILES) {
    fprintf(stderr, "Error: Too many files specified. Max allowed is 100.\n");
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}