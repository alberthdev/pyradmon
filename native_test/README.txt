Crazy Experiment README
===========================================================================
Crazy experiment... gone right!

All important files (read_dummy.f90, kinds.F90, and test_dummy.f90) are linked
from your directory, /gpfsm/dnb02/wrmccart/new_radmon/read_dummy-v2. This is
to ensure that we are indeed using untouched code!

Quick Commands:
---------------------------------------------------------------
Working experimental code:
    BUILD WORKING EXPERIMENT:
        make c-exp
    RUN WORKING EXPERIMENT:
        ./crazy-exp

Semi-working (but failed) experimental code:
    BUILD FAILED EXPERIMENT:
        make
    RUN FAILED EXPERIMENT:
        ./crazy
(in case you want to see how far I got with the old code!)

For both:
    CLEAN ALL (both working and not working binaries):
        make clean

Files of Interest:
---------------------------------------------------------------
crazy-exp.c - C file to wrap and call Fortran code
fcwrap.f90  - Fortran/C Array and Pointer Wrapper
Makefile    - build file

Technical Details:
---------------------------------------------------------------
The failed code and the working code share the first part of the codebase.
It diverges when we reach our first print_array call.

The method used to link C and Fortran (and inevitably, Python) is to compile
and treat the Fortran 90 code as a shared library (e.g. a .so file).

In our Makefile, we do:
    # OUTPUT: kinds.o kinds.mod
    ifort -g -free -fPIC -c kinds.F90 -D_REAL8
    
    # OUTPUT: read_dummy.o read_dummy.mod
    # This pulls the kinds.mod file in, compiled from the above command
    ifort -g -free -fPIC -c read_dummy.f90
    
    # OUTPUT: read_dummy.so
    ifort -g -fPIC -shared -o read_dummy.so read_dummy.o

Then, in crazy.c and crazy-exp.c, we use the dynamic library opener to open
the shared library and make the calls to the program. Some quick example
initialization code below (note - only for show, may not actually compile - see
crazy.c/crazy-exp.c for actual implementation!):
    #include <dlfcn.h>
    int main() {
        // The shared library file name.
        char file_name[80] = "./read_dummy.so";
        // This variable is our handle for the shared library.
        void *read_dummy;
        // This variable is our function pointer for fetching functions from
        // the shared library.
        void *(*get_data_)(int *inlun, data_list *dat);
        
        // Open the shared library!
        read_dummy = dlopen (file_name, RTLD_NOW);
        
        // Sanity check!
        if (!read_dummy)
        {
            fatal ("Cannot load %s: %s", file_name, dlerror ());
        }
        
        printf("Successfully loaded %s!\n", file_name);
        
        // Try to find the symbol and associate it with our function pointer.
        get_data_ = dlsym(read_dummy, "read_dummy_mp_get_data_");
        err_str = dlerror();
        // Did we succeed?
        if (err_str) {
            fatal("Cannot find get_data_ in %s: %s", file_name, err_str);
        }
    }

One other thing - calling subroutines from C are *ALWAYS* called by reference.
Calls therefore look like this:
    data_list *dat;
    int ndata = 15;
    // Note that dat does not have a & because it's already a pointer.
    get_data_(&ifn,dat);

Knowing that, we can make standard calls to Fortran code. Yay!

...or not. Once you encouter Fortran code that uses assumed shaped arrays as
arguments, things get messy:
    real(r_single),dimension(:),intent(inout),allocatable :: array

Every time, no matter how you pass the array pointer in, the code will crash.
The solution? We have some wrapper Fortran code that converts our C pointer
into a Fortran pointer!

Essentially, we call C_F_POINTER to convert our C pointer into a Fortran
pointer, as well as give it a size.
    call C_F_POINTER (cptr_to_array, array, [n_elements])

(See fcwrap.f90 for details.)

Once we have that, we compile this module into a shared library. (We'd love to
compile it as a static library, but you would need to use bind(c), and Intel's
compiler freaks out when there's a bind(c), and a dimension(:) in the same
subroutine....)

Once that's done, we call the function to convert the C array to a Fortran
pointer array, and then we pass our shiny Fortran pointer array into our
shaped array functions:
    void *cur_array_fortran;
    fortify_c_array_float_(&cur_array, &(head->ndata), &cur_array_fortran);
    print_array_(&cur_array_fortran,&(head->ndata));

Does this stay consistent everywhere? Not always. In fact, write_array_ requires
a Fortran array, but it has a fixed size! Therefore, it is NOT a pointer to a pointer:
    write_array_(&lun,fn,cur_array_fortran,&(head->ndata));

(To be honest, no idea why it acts that way...)

Now we know enough to call the Fortran subroutines - and it works!


