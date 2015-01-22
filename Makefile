CFLG= -Wall
all: runtime.a test

runtime.a: runtime.o hashtable.o hashtable_itr.o hashtable_utility.o
	ar -rcs $@ $^

clean:
	rm -f $(EXE) *.o *.a

runtime.o: runtime/runtime.c runtime/runtime.h
	gcc -c $(CFLG) $< -m32
hashtable.o: runtime/hashtable.c runtime/hashtable.h
	gcc -c $(CFLG) $< -m32
hashtable_itr.o: runtime/hashtable_itr.c runtime/hashtable_itr.h
	gcc -c $(CFLG) $< -m32
hashtable_utility.o: runtime/hashtable_utility.c runtime/hashtable_utility.h
	gcc -c $(CFLG) $< -m32

test: test.s runtime.a
	gcc test.s runtime.a -m32 -lm -o test
