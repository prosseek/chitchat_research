    # starter code
    function_call MAIN
    stop
MAIN:
    print "if test"
    # if (10 + 20 == 30)
    push 10
    push 20
    iadd
    push 30
    cmp
    # zero - different
    jfalse DIFFERENT
    print "same"
    jmp   END
DIFFERENT:
    print "different"
END:
    # add return value
    push 0
    return 0
