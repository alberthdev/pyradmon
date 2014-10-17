include Makefile.inc

SRC=src/
DIRS=$(SRC)

all: gsidiag_bin2txt.x

gsidiag_bin2txt.x:
	-for d in $(DIRS); do (cd $$d; $(MAKE) all); done
	$(F90) $(SRC)/kinds.o $(SRC)/read_diag.o $(SRC)/gsidiag_bin2txt.o -o gsidiag_bin2txt.x

clean:
	/bin/rm -f *.o *.mod *.x
	-for d in $(DIRS); do (cd $$d; $(MAKE) clean ); done

realclean:
	$(MAKE) clean
	/bin/rm -f Makefile.inc example_data/x0014_so14.diag_amsua_n18_ges.20140201_00z.txt

distclean: realclean
