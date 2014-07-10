from ctypes import *
rd = cdll.LoadLibrary("./read_dummy.so")
rd.read_dummy_mp_get_header_
