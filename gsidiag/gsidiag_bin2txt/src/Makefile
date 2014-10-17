include ../Makefile.inc

# Fortran compiler:
FFLAGS=-c $(FFLAGS_IN)

all: kinds.o read_diag.o gsidiag_bin2txt.o

kinds.o: $(GSI_LOC)/kinds.F90
	$(F90) $(FFLAGS) $<

read_diag.o: $(GSI_LOC)/read_diag.f90
	$(F90) $(FFLAGS) $<

gsidiag_bin2txt.o: gsidiag_bin2txt.f90
	$(F90) $(FFLAGS) $<

clean:
	rm -rf *.o *.x *.mod


