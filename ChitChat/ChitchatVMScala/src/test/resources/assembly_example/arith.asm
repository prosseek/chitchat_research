    function_call MAIN
    stop
MAIN:
    push 101
    push 202
    iadd
    pop $temp
    print $temp
    print "stop the program and bye"
    push $temp

    return 0