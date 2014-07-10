module fcwrap
    use, intrinsic :: iso_c_binding
    implicit none

    !interface
    ! function make_array_int(n_elements) bind(C)
    !   import ! Make iso_c_binding visible here
    !   type(C_PTR) :: make_array
    !   integer(C_INT), value, intent(IN) :: n_elements
    ! end function make_array
    !end interface
    
    public :: fortify_c_array_int
    public :: fortify_c_array_float
    public :: fortify_c_array_double
    
    contains
        subroutine fortify_c_array_int(cptr_to_array, n_elements, array)
            type(C_PTR), intent(in)                 :: cptr_to_array
            integer, intent(in)                     :: n_elements ! Number of elements
            integer(C_INT), pointer, intent(out)    :: array(:) => NULL()
            
            ! Call C function to create and populate an array
            !!!!!! cptr_to_array = make_array(n_elements)
            ! Convert to Fortran pointer to array of n_elements elements
            call C_F_POINTER (cptr_to_array, array, [n_elements])
            ! Print value
            !print *, array
        end subroutine fortify_c_array_int
        
        subroutine fortify_c_array_float(cptr_to_array, n_elements, array)
            type(C_PTR), intent(in)                 :: cptr_to_array
            integer, intent(in)                     :: n_elements ! Number of elements
            real(C_FLOAT), pointer, intent(out)     :: array(:) => NULL()
            
            ! Call C function to create and populate an array
            !!!!!! cptr_to_array = make_array(n_elements)
            ! Convert to Fortran pointer to array of n_elements elements
            call C_F_POINTER (cptr_to_array, array, [n_elements])
            ! Print value
            !print *, array
        end subroutine fortify_c_array_float
        
        subroutine fortify_c_array_double(cptr_to_array, n_elements, array)
            type(C_PTR), intent(in)                 :: cptr_to_array
            integer, intent(in)                     :: n_elements ! Number of elements
            real(C_DOUBLE), pointer, intent(out)    :: array(:) => NULL()
            
            ! Call C function to create and populate an array
            !!!!!! cptr_to_array = make_array(n_elements)
            ! Convert to Fortran pointer to array of n_elements elements
            call C_F_POINTER (cptr_to_array, array, [n_elements])
            ! Print value
            !print *, array
        end subroutine fortify_c_array_double
end module fcwrap
