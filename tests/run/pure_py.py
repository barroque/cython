import cython

is_compiled = cython.compiled

NULL = 5
_NULL = NULL

def test_sizeof():
    """
    >>> test_sizeof()
    True
    True
    True
    True
    True
    """
    x = cython.declare(cython.bint)
    print(cython.sizeof(x) == cython.sizeof(cython.bint))
    print(cython.sizeof(cython.char) <= cython.sizeof(cython.short) <= cython.sizeof(cython.int) <= cython.sizeof(cython.long) <= cython.sizeof(cython.longlong))
    print(cython.sizeof(cython.uint) == cython.sizeof(cython.int))
    print(cython.sizeof(cython.p_int) == cython.sizeof(cython.p_double))
    if cython.compiled:
        print(cython.sizeof(cython.char) < cython.sizeof(cython.longlong))
    else:
        print(cython.sizeof(cython.char) == 1)

def test_declare(n):
    """
    >>> test_declare(100)
    (100, 100)
    >>> test_declare(100.5)
    (100, 100)
    >>> test_declare(None) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    """
    x = cython.declare(cython.int)
    y = cython.declare(cython.int, n)
    if cython.compiled:
        cython.declare(xx=cython.int, yy=cython.long)
        i = cython.sizeof(xx)
    ptr = cython.declare(cython.p_int, cython.address(y))
    return y, ptr[0]

@cython.locals(x=cython.double, n=cython.int)
def test_cast(x):
    """
    >>> test_cast(1.5)
    1
    """
    n = cython.cast(cython.int, x)
    return n

@cython.locals(x=cython.int, y=cython.p_int)
def test_address(x):
    """
    >>> test_address(39)
    39
    """
    y = cython.address(x)
    return y[0]

## CURRENTLY BROKEN - FIXME!!
## Is this test make sense? Implicit conversion in pure Python??

## @cython.locals(x=cython.int)
## @cython.locals(y=cython.bint)
## def test_locals(x):
##     """
##     >>> test_locals(5)
##     True
##     """
##     y = x
##     return y

def test_with_nogil(nogil):
    """
    >>> raised = []
    >>> class nogil(object):
    ...     def __enter__(self):
    ...         pass
    ...     def __exit__(self, exc_class, exc, tb):
    ...         raised.append(exc)
    ...         return exc_class is None

    >>> test_with_nogil(nogil())
    WORKS
    True
    >>> raised
    [None]
    """
    result = False
    with nogil:
        print("WORKS")
        with cython.nogil:
            result = True
    return result

MyUnion = cython.union(n=cython.int, x=cython.double)
MyStruct = cython.struct(is_integral=cython.bint, data=MyUnion)
MyStruct2 = cython.typedef(MyStruct[2])

def test_struct(n, x):
    """
    >>> test_struct(389, 1.64493)
    (389, 1.64493)
    """
    a = cython.declare(MyStruct2)
    a[0] = MyStruct(is_integral=True, data=MyUnion(n=n))
    a[1] = MyStruct(is_integral=False, data={'x': x})
    return a[0].data.n, a[1].data.x

import cython as cy
from cython import declare, cast, locals, address, typedef, p_void, compiled
from cython import declare as my_declare, locals as my_locals, p_void as my_void_star, typedef as my_typedef, compiled as my_compiled

@my_locals(a=cython.p_void)
def test_imports():
    """
    >>> test_imports()
    (True, True)
    """
    a = cython.NULL
    b = declare(p_void, cython.NULL)
    c = my_declare(my_void_star, cython.NULL)
    d = cy.declare(cy.p_void, cython.NULL)

    return a == d, compiled == my_compiled

## CURRENTLY BROKEN - FIXME!!

# MyStruct3 = typedef(MyStruct[3])
# MyStruct4 = my_typedef(MyStruct[4])
# MyStruct5 = cy.typedef(MyStruct[5])

def test_declare_c_types(n):
    """
    >>> test_declare_c_types(0)
    >>> test_declare_c_types(1)
    >>> test_declare_c_types(2)
    """
    #
    b00 = cython.declare(cython.bint, 0)
    b01 = cython.declare(cython.bint, 1)
    b02 = cython.declare(cython.bint, 2)
    #
    i00 = cython.declare(cython.uchar, n)
    i01 = cython.declare(cython.char, n)
    i02 = cython.declare(cython.schar, n)
    i03 = cython.declare(cython.ushort, n)
    i04 = cython.declare(cython.short, n)
    i05 = cython.declare(cython.sshort, n)
    i06 = cython.declare(cython.uint, n)
    i07 = cython.declare(cython.int, n)
    i08 = cython.declare(cython.sint, n)
    i09 = cython.declare(cython.slong, n)
    i10 = cython.declare(cython.long, n)
    i11 = cython.declare(cython.ulong, n)
    i12 = cython.declare(cython.slonglong, n)
    i13 = cython.declare(cython.longlong, n)
    i14 = cython.declare(cython.ulonglong, n)

    i20 = cython.declare(cython.Py_ssize_t, n)
    i21 = cython.declare(cython.size_t, n)
    #
    f00 = cython.declare(cython.float, n)
    f01 = cython.declare(cython.double, n)
    f02 = cython.declare(cython.longdouble, n)
    #
    #z00 = cython.declare(cython.complex, n+1j)
    #z01 = cython.declare(cython.floatcomplex, n+1j)
    #z02 = cython.declare(cython.doublecomplex, n+1j)
    #z03 = cython.declare(cython.longdoublecomplex, n+1j)

@cython.ccall
@cython.returns(cython.double)
def c_call(x):
    """
    Test that a declared return type is honoured when compiled.

    >>> result, return_type = call_ccall(1)

    >>> (not is_compiled and 'double') or return_type
    'double'
    >>> (is_compiled and 'int') or return_type
    'int'

    >>> (not is_compiled and 1.0) or result
    1.0
    >>> (is_compiled and 1) or result
    1
    """
    return x

def call_ccall(x):
    ret = c_call(x)
    return ret, cython.typeof(ret)
