    function_call MAIN
    stop

MAIN:
    print "function call2 test"
    push 10
    push 20
    function_call_stack F1 2
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

    push $temp
    push $temp
    push $temp
    function_call_stack F2 3
    return 2
F2:
    load $bp - 1
    load $bp - 2
    load $bp - 3
    iadd
    iadd
    return 3
