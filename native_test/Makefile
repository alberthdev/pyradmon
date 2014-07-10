# Constants
BOLD  = "\033[1m"
NBOLD = "\033[0m"
ECHO  = /bin/echo -e

%.o: %.mod

.PHONY: clean pre-python pre-c pre-fortran pre-python c fortran python all-done

all: python c fortran all-done

all-done:
	@$(ECHO) $(BOLD)"Done!"$(NBOLD)

#######################################################################
c: pre-c crazy

pre-c:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building C wrapper...                         ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

crazy.o: crazy.c
	@$(ECHO) $(BOLD)" ** Compiling C program..."$(NBOLD)
	icc -g -c crazy.c

crazy: read_dummy.so crazy.o
	@$(ECHO) $(BOLD)" ** Compiling Fortran + C program -> final executable..."$(NBOLD)
	#icc -o test test.o read_dummy.o -lifcore -limf
	#ifort -o test test.o read_dummy.o -nofor-main
	icc -g -o crazy crazy.o
#######################################################################
c-exp: pre-c-exp crazy-exp

pre-c-exp:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building C wrapper (EXPERIMENTAL)...          ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

# crazy.o: crazy.c [DEP]

crazy-exp.o: crazy-exp.c
	@$(ECHO) $(BOLD)" ** Compiling C program (EXPERIMENTAL)..."$(NBOLD)
	icc -g -c crazy-exp.c

crazy-exp: read_dummy.so fcwrap.so crazy-exp.o
	@$(ECHO) $(BOLD)" ** Compiling Fortran + C program -> final executable..."$(NBOLD)
	#icc -o test test.o read_dummy.o -lifcore -limf
	#ifort -o test test.o read_dummy.o -nofor-main
	icc -g -o crazy-exp crazy-exp.o

fcwrap.o: fcwrap.f90
	ifort -g -free -fPIC -c fcwrap.f90

fcwrap.so: fcwrap.o
	ifort -g -fPIC -shared -o fcwrap.so fcwrap.o
#######################################################################
fortran: pre-fortran test_dummy.x

pre-fortran:
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)
	@$(ECHO) $(BOLD)"= Building pure Fortran test...                 ="$(NBOLD)
	@$(ECHO) $(BOLD)"================================================="$(NBOLD)

test_dummy.x: read_dummy.mod test_dummy.o
	ifort -o test_dummy.x test_dummy.o kinds.o read_dummy.o

test_dummy.o:
	ifort -g -free -fPIC -c test_dummy.f90
#######################################################################
read_dummy.o: read_dummy.mod
kinds.o: kinds.mod

read_dummy.so: read_dummy.o
	ifort -g -fPIC -shared -o read_dummy.so read_dummy.o

read_dummy.mod: kinds.mod read_dummy.f90
	@$(ECHO) $(BOLD)" ** Compiling main Fortran program..."$(NBOLD)
	ifort -g -free -fPIC -c read_dummy.f90

kinds.mod: kinds.F90
	@$(ECHO) $(BOLD)" ** Compiling kinds Fortran program..."$(NBOLD)
	ifort -g -free -fPIC -c kinds.F90 -D_REAL8_
#######################################################################
clean:
	@$(ECHO) $(BOLD)" ** Cleaning source directory..."$(NBOLD)
	rm -f *.mod *.x *.pyc *.o *.so test read_dummy.py read_dummy_wrap.c test.h test.output.binary

clean-c:
	@$(ECHO) $(BOLD)" ** Removing objects from source directory..."$(NBOLD)
	rm -f *.mod *.o *.so
