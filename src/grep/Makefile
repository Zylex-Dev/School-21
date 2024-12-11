CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Werror -D_POSIX_C_SOURCE=201709L
SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)
EXEC = s21_grep

all: clang cppcheck $(EXEC) valgrind test

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(EXEC)

%.o: %.c grep.h
	$(CC) $(CFLAGS) -c $< -o $@

test: $(EXEC)
	@echo "Running tests..."
	@echo ""
	@../common/grep_tests/test_script.sh
	@echo ""
	@echo "Testing is completed"

valgrind:
	valgrind --tool=memcheck --leak-check=yes  ./$(EXEC)

cppcheck:
	cppcheck --enable=all --suppress=missingIncludeSystem $(SRC)

clang:
	clang-format -n $(SRC) grep.h
	clang-format -i $(SRC) grep.h

clean: 
	rm -rf *.out *.o $(EXEC)

rebuild: clean all