CFLG= -Wall
all: runtime.o hashtable.o hashtable_itr.o hashtable_utility.o

clean:
	rm -f $(EXE) *.o *.a

hashtable.o: runtime/hashtable.c runtime/hashtable.h
	gcc -c $(CFLG) $< -m32
hashtable_itr.o: runtime/hashtable_itr.c runtime/hashtable_itr.h
	gcc -c $(CFLG) $< -m32
hashtable_utility.o: runtime/hashtable_utility.c runtime/hashtable_utility.h
	gcc -c $(CFLG) $< -m32
runtime.o: runtime/runtime.c runtime/runtime.h
	gcc -c $(CFLG) $< -m32