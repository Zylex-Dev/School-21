#include "s21_cat.h"

void process_file(FILE *temp_file, void (*process_line)(const char *, FILE *)) {
  rewind(temp_file);
  char buffer[BUFFER_SIZE];
  FILE *temp_out = tmpfile();

  if (temp_out == NULL) {
    printf("Error creating temporary output file");
  } else {
    while (fgets(buffer, BUFFER_SIZE, temp_file) != NULL) {
      process_line(buffer, temp_out);
    }

    rewind(temp_file);
    rewind(temp_out);
    freopen(NULL, "w+", temp_file);

    while (fgets(buffer, BUFFER_SIZE, temp_out) != NULL) {
      fputs(buffer, temp_file);
    }

    fclose(temp_out);
  }
}

void process_line_n(const char *line, FILE *output) {
  static int line_number = 1;
  fprintf(output, "%6d\t%s", line_number, line);
  line_number++;
}

void process_line_b(const char *line, FILE *output) {
  if (strlen(line) > 1) {
    static int line_number = 1;
    fprintf(output, "%6d\t%s", line_number, line);
    line_number++;
  } else {
    fputs("\n", output);
  }
}

void process_line_t(const char *line, FILE *output) {
  const char *ch = line;
  while (*ch != '\0') {
    if (*ch == '\t') {
      fputs("^I", output);
    } else {
      fputc(*ch, output);
    }
    ch++;
  }
}

void process_line_v(const char *line, FILE *output) {
  while (*line != '\0') {
    unsigned char c = (unsigned char)*line;
    if (c >= 32 && c <= 126) {
      fputc(c, output);
    } else if (c == '\n' || c == '\t') {
      fputc(c, output);
    } else if (c == 127) {
      fputs("^?", output);
    } else if (c < 32) {
      fprintf(output, "^%c", c + 64);
    } else if (c >= 128) {
      fputs("M-", output);
      if (c < 160) {
        fprintf(output, "^%c", (c - 128) + 64);
      } else {
        fputc(c - 128, output);
      }
    }
    line++;
  }
}

void process_line_e(const char *line, FILE *output) {
  char temp[BUFFER_SIZE];
  strncpy(temp, line, BUFFER_SIZE - 1);  // copies line to temp
  size_t len = strlen(temp);

  if (len > 0 && temp[len - 1] == '\n') {
    temp[len - 1] = '\0';
    fprintf(output, "%s$\n", temp);
  } else {
    fprintf(output, "%s", temp);
  }
}

void process_line_s(const char *line, FILE *output) {
  static int prev_is_empty = 0;

  if (strcmp(line, "\n") == 0 || strcmp(line, "\r\n") == 0) {
    // line is empty
    if (!prev_is_empty) {  // if previous line wasn`t empty - write (if
                           // was - nothing)
      fputs(line, output);
    }
    // put flag - current line is empty
    prev_is_empty = 1;
  } else {  // if line isn`t empty
    fputs(line, output);
    prev_is_empty = 0;  // drops flag
  }
}

int is_file_exist(const char *fname) {
  FILE *file;
  if ((file = fopen(fname, "r"))) {
    fclose(file);
    return 1;
  }
  return 0;
}

void copy_file_to_temp(const char *source_file, FILE *temp_file) {
  FILE *source = fopen(source_file, "r");
  if (source == NULL) {
    printf("Error opening source file");
  } else {
    char buffer[BUFFER_SIZE];
    while (fgets(buffer, BUFFER_SIZE, source) !=
           NULL) {  // write src file to temp
      fputs(buffer, temp_file);
    }
  }
  fclose(source);     // close src file
  rewind(temp_file);  // put pointer tmp file to the start
}

void print_temp_file(FILE *temp_file) {
  rewind(temp_file);
  char buffer[BUFFER_SIZE];
  while (fgets(buffer, BUFFER_SIZE, temp_file) != NULL) {
    printf("%s", buffer);
  }
}

void n_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_n);
}

void b_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_b);
}

void t_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_t);
}

void v_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_v);
}

void e_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_e);
}

void s_flag_realization(FILE *temp_file) {
  process_file(temp_file, process_line_s);
}

// function that opens and prints file
void process_file_with_flags(char const *source_file, int flag_b, int flag_e,
                             int flag_n, int flag_s, int flag_t, int flag_v,
                             int flag_E, int flag_T) {
  if (is_file_exist(source_file)) {
    FILE *temp = tmpfile();  // creates tmp file (already opened)
    if (temp == NULL) {
      printf("Error creating temporary file");
    } else {
      copy_file_to_temp(source_file, temp);

      if (flag_s) {
        s_flag_realization(temp);
      }
      if (flag_b) {
        b_flag_realization(temp);
      } else if (flag_n) {
        n_flag_realization(temp);
      }
      if (flag_e) {
        e_flag_realization(temp);
        v_flag_realization(temp);
      }
      if (flag_t) {
        t_flag_realization(temp);
        v_flag_realization(temp);
      }
      if (flag_v) {
        v_flag_realization(temp);
      }
      if (flag_E) {
        e_flag_realization(temp);
      }
      if (flag_T) {
        t_flag_realization(temp);
      }

      // output of temp file
      print_temp_file(temp);
      fclose(temp);
    }
  } else {
    printf("File doesn`t exist\n");
  }
}

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: ./s21_cat [OPTION]... [FILE]...\n");
  } else {
    // flags parsing
    int flag_b = 0, flag_e = 0, flag_n = 0, flag_s = 0, flag_t = 0, flag_v = 0;
    int flag_E = 0, flag_T = 0;

    struct option long_options[] = {
        {"number-nonblank", no_argument, 0, 'b'},
        {"number", no_argument, 0, 'n'},
        {"squeeze-blank", no_argument, 0, 's'},
        {"show-ends", no_argument, 0, 'E'},
        {"show-tabs", no_argument, 0, 'T'},
        {"show-nonprinting", no_argument, 0, 'v'},
        {NULL, 0, NULL, 0}  // end of arr
    };

    int rez = 0;
    int option_index = 0;  // index for long options
    int error_flag = 0;
    opterr = 0;
    while ((rez = getopt_long(argc, argv, "benstvET", long_options,
                              &option_index)) != -1) {
      switch (rez) {
        case 'b':
          flag_b = 1;
          break;
        case 'e':
          flag_e = 1;
          flag_v = 1;
          break;
        case 'n':
          flag_n = 1;
          break;
        case 's':
          flag_s = 1;
          break;
        case 't':
          flag_t = 1;
          flag_v = 1;
          break;
        case 'v':
          flag_v = 1;
          break;
        case 'E':
          flag_E = 1;
          flag_e = 0;
          flag_v = 0;
          break;
        case 'T':
          flag_T = 1;
          flag_t = 0;
          flag_v = 0;
          break;
        case '?':
          printf("Unkown option: %c\n", optopt);
          error_flag = 1;
          break;

        default:
          break;
      }
    }

    if (!error_flag) {
      for (int i = optind; i < argc; i++) {
        process_file_with_flags(argv[i], flag_b, flag_e, flag_n, flag_s, flag_t,
                                flag_v, flag_E, flag_T);
      }
    }
  }

  return 0;
}