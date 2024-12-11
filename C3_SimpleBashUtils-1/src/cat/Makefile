CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Werror -D_POSIX_C_SOURCE=201709L

all: clang cppcheck s21_cat valgrind

s21_cat: clean
	$(CC) $(CFLAGS) s21_cat.c s21_cat.h -o s21_cat

valgrind:
	valgrind --tool=memcheck --leak-check=yes  ./s21_cat

test: s21_cat
	@echo "Running tests..."
	@echo ""
	@../common/cat_tests/test_script.sh
	@echo ""
	@echo "Testing is completed"

cppcheck:
	cppcheck --enable=all --suppress=missingIncludeSystem s21_cat.c

clang:
	clang-format -n s21_cat.c s21_cat.h
	clang-format -i s21_cat.c s21_cat.h

clean: 
	rm -rf *.out *.o s21_cat

rebuild: clean all