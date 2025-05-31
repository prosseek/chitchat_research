# + schema x = (name , event , (sensor, value)+ )

    function_call SENSORS
    stop

SENSORS:
    read name
    jpeekfalse END
    register name

    read event
    jpeekfalse END
    register event

    f ITER
    jpeekfalse END
    pop $temp

    push_summary
END:
    return 0

# (sensor, value)+
ITER:
    # i = 0
    # one local variable
    # i == bp + 2 -> first variable
    push 0

    # assignment i = 0
    push 0
    store $bp + 2

    # there should be at least one sensor data
    load $bp + 2
    pop $temp
    read sensor $temp
    jpeekfalse ERRORENDLOOP
    register sensor $temp
    read value $temp
    jpeekfalse ERRORENDLOOP
    register value $temp
START:
    # while (true)
    #   i += 1
    #   read sensor i
    #   read value  i

    # i = i + 1
    load $bp + 2
    push 1
    iadd

    store $bp + 2
    load $bp + 2
    pop $temp

    read sensor $temp
    jpeekfalse ENDLOOP
    register sensor $temp

    read value $temp
    jpeekfalse ENDLOOP
    register value $temp

    jmp START

ERRORENDLOOP:
    # false - local_variable - ... (before in stack)
    # local_variable - false - ... (after in stack)
    swap
ENDLOOP:
    # remove a local variable
    pop
    r 0