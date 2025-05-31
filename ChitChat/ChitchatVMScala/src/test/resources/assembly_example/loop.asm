    function_call MAIN
    stop

MAIN:
    print "loop test"
    # i = 0
    # limit = 10
    # two local variables
    # i == bp + 2 -> first variable
    # limit == bp + 3 -> second variable
    push 0
    push 0

    # assignment i = 0
    push 0
    store $bp + 2

    # assignment limit = 10
    push 10
    store $bp + 3
START:
    # while (i < limit)
    load $bp + 2
    load $bp + 3
    less
    jfalse END

    # temp <- i
    load $bp + 2
    pop $temp
    print $temp

    # i = i + 1
    load $bp + 2
    push 1
    iadd
    store $bp + 2

    jmp START
END:
    print "out of loop"
    # remove two local variables
    pop
    pop

    push 0
    return 0
