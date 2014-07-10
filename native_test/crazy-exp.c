#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <dlfcn.h>
#include "crazy.h"

//#include "fcwrap.h"

// read_dummy._
// read_dummy_mp_get_data_
// read_dummy_mp_get_header_
// read_dummy_mp_inc_mean_
// read_dummy_mp_init_dummy_
// read_dummy_mp_print_array_
// read_dummy_mp_read_array_
// read_dummy_mp_ret_mean_
// read_dummy_mp_ret_mean_from_array_
// read_dummy_mp_set_ndata_
// read_dummy_mp_test_init_
// read_dummy_mp_write_array_

/*void init_dummy();
void set_ndata(int *nd);
void test_init();
void inc_mean(float *ob, mean_type *mean);
void print_array(float *array, int *ndata);
void write_array(int *lun, char *filename, float *array, int *ndata);
void read_array(int *lun, char *filename, float *array, int *ndata);
void get_header(int *inlun, header_list *head);
void get_data(int *inlun, data_list *dat);
float ret_mean(mean_type *mean);
float ret_mean_from_array(float *array, int *ndata);*/

char file_name[80] = "./read_dummy.so";
char *err_str;
void *read_dummy;
void *(*init_dummy_)();
void *(*get_data_)(int *inlun, data_list *dat);
void *(*get_header_)(int *inlun, header_list *head);
void *(*inc_mean_)(float *ob, mean_type *mean);
void *(*print_array_)(float *array, int *ndata);
void *(*read_array_)(int *lun, char *filename, float *array, int *ndata);
float (*ret_mean_)(mean_type *mean);
float (*ret_mean_from_array_)(float *array, int *ndata);
void *(*set_ndata_)(int *nd);
void *(*test_init_)();
void *(*write_array_)(int *lun, char *filename, float *array, int *ndata);

char file_name_2[80] = "./fcwrap.so";
void *fcwrap;
void *(*get_data_)(int *inlun, data_list *dat);
void *(*fortify_c_array_int_)(int *cptr_to_array, int *n_elements, void *array);
void *(*fortify_c_array_float_)(float *cptr_to_array, int *n_elements, void *array);
void *(*fortify_c_array_double_)(double *cptr_to_array, int *n_elements, void *array);

void fatal( const char* format, ... ) {
    va_list args;
    fprintf( stderr, "Error: " );
    va_start( args, format );
    vfprintf( stderr, format, args );
    va_end( args );
    fprintf( stderr, "\n" );
    exit(1);
}

void init_module() {
    // FCWRAP
    printf(" * Attempting to load fcwrap module...\n");
    fcwrap = dlopen (file_name_2, RTLD_NOW);
    if (!fcwrap)
    {
        fatal ("Cannot load %s: %s", file_name_2, dlerror ());
    }
    printf("  ** Successfully loaded %s!\n", file_name_2);
    
    fortify_c_array_int_ = dlsym(fcwrap, "fcwrap_mp_fortify_c_array_int_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_int_ in %s: %s", file_name_2, err_str);
    }
    
    fortify_c_array_float_ = dlsym(fcwrap, "fcwrap_mp_fortify_c_array_float_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_float_ in %s: %s", file_name_2, err_str);
    }
    
    fortify_c_array_double_ = dlsym(fcwrap, "fcwrap_mp_fortify_c_array_double_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_double_ in %s: %s", file_name_2, err_str);
    }
    
    printf("  ** Successfully loaded all functions for fcwrap!\n");
    
    // READ_DUMMY
    printf(" * Attempting to load read_dummy module...\n");
    read_dummy = dlopen (file_name, RTLD_NOW);
    if (!read_dummy)
    {
        fatal ("Cannot load %s: %s", file_name, dlerror ());
    }
    printf("  ** Successfully loaded %s!\n", file_name);
    
    init_dummy_ = dlsym(read_dummy, "read_dummy_mp_init_dummy_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find init_dummy_ in %s: %s", file_name, err_str);
    }
    
    get_data_ = dlsym(read_dummy, "read_dummy_mp_get_data_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find get_data_ in %s: %s", file_name, err_str);
    }
    
    get_header_ = dlsym(read_dummy, "read_dummy_mp_get_header_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find get_header_ in %s: %s", file_name, err_str);
    }
    
    inc_mean_ = dlsym(read_dummy, "read_dummy_mp_inc_mean_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find inc_mean_ in %s: %s", file_name, err_str);
    }
    
    print_array_ = dlsym(read_dummy, "read_dummy_mp_print_array_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find print_array_ in %s: %s", file_name, err_str);
    }
    
    read_array_ = dlsym(read_dummy, "read_dummy_mp_read_array_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find read_array_ in %s: %s", file_name, err_str);
    }
    
    ret_mean_ = dlsym(read_dummy, "read_dummy_mp_ret_mean_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find ret_mean_ in %s: %s", file_name, err_str);
    }
    
    ret_mean_from_array_ = dlsym(read_dummy, "read_dummy_mp_ret_mean_from_array_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find ret_mean_from_array_ in %s: %s", file_name, err_str);
    }
    
    set_ndata_ = dlsym(read_dummy, "read_dummy_mp_set_ndata_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find set_ndata_ in %s: %s", file_name, err_str);
    }
    
    test_init_ = dlsym(read_dummy, "read_dummy_mp_test_init_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find test_init_ in %s: %s", file_name, err_str);
    }
    
    write_array_ = dlsym(read_dummy, "read_dummy_mp_write_array_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find write_array_ in %s: %s", file_name, err_str);
    }
    
    printf("  ** Successfully loaded all functions for read_dummy!\n");
    
    printf(" * All modules loaded!\n");
    printf("***********************************************************\n");
    printf("* Actual Fortran code execution begins below...           *\n");
    printf("***********************************************************\n");
}

int main() {
    init_module();
    
    header_list *head;
    data_list *dat;
             
    mean_type *cur_mean;
    float *cur_array, *array_from_file = NULL;
    
    head      = (header_list *) malloc(sizeof(header_list));
    dat       = (data_list *)   malloc(sizeof(data_list));
    cur_mean  = (mean_type *)   malloc(sizeof(mean_type));
    
    char fn[120] = "test.output.binary";
    
    int i, ifn, lun, ndata_from_file;
    
    init_dummy_();
    
    int ndata = 15;
    
    set_ndata_(&ndata);  //just for the heck of it, increase ndata to 15
    
    get_header_(&ifn,head); // First, we 'read' the header 
    
    printf("%25s %20s\n", "head%header_title=",head->header_title);
    printf("%25s %10i\n", "head%ndata=",head->ndata);
    printf("%25s %10i\n", "head%nchan=",head->nchan);
    printf("%25s %10.3f\n", "head%dummy=",head->dummy);
    
    cur_array = (float *) malloc(sizeof(float) * (head->ndata));
    
    for(i=1; i <= head->ndata; i++) {          // then we loop over the ndata from the header
        get_data_(&ifn,dat);   //   and read each data point in a loop
        printf("%25s %10.3f\n", "dat%obs=",dat->obs);
        printf("%25s %10.3f\n", "dat%error=",dat->error);
        inc_mean_(&(dat->obs), cur_mean); // sequentially calculate mean
        cur_array[i-1] = dat->obs;
    }
    
    void *cur_array_fortran;
    
    fortify_c_array_float_(&cur_array, &(head->ndata), &cur_array_fortran);
    print_array_(&cur_array_fortran,&(head->ndata));
    
    //print_array_(&cur_array,&(head->ndata));
    
    printf(" Mean from mean_type:            %10.6f\n",ret_mean_(cur_mean)); // return mean from sequential calculation
    printf(" Mean from ret_mean_from_array:  %10.6f\n",ret_mean_from_array_(&cur_array_fortran,&(head->ndata))); //return mean from instantaneous array calc
    
    lun = 123;
    
    write_array_(&lun,fn,cur_array_fortran,&(head->ndata));           // write array to 'self-describing' binary file (first element ndata, second element array(ndata) )
    
    void *array_from_file_fortran;
    fortify_c_array_float_(&array_from_file, &(head->ndata), &array_from_file_fortran);
    
    read_array_(&lun,fn,&array_from_file_fortran,&ndata_from_file); // read array from 'self-describing' binary file
    
    print_array_(&array_from_file_fortran,&ndata_from_file);
}
