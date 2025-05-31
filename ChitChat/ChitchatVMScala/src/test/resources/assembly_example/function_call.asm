    function_call MAIN
    stop

MAIN:
    print "function call test"
    function_call F1 10 20
    pop $temp
    print $temp
    # for assertion pass, the return value of this script should be in the stack
    push $temp
    return 0
F1:
    load $bp - 1
    load $bp - 2
    iadd
    pop $temp
    function_call F2 $temp $temp $temp
    return 2
F2:
    load $bp - 1
    load $bp - 2
    load $bp - 3
    iadd
    iadd
    return 3
