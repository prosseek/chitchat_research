# +schema sensors = (a, b, c)
# startup code
    jmp START

_READ_TO_REG:
    load $bp - 1
    pop $temp
    read $temp
    jpeekfalse _READ_TO_REG_END
    register $temp
    push true
_READ_TO_REG_END:
    return 1

# compiler returns the main function caller and callee        
START:
    f sensors
    stop
        
sensors: 
    # a
    f _READ_TO_REG a
    jpeekfalse sensors_END
    pop $temp

    # b
    f _READ_TO_REG b
    jpeekfalse sensors_END
    pop $temp

    # c
    f _READ_TO_REG c
    jpeekfalse sensors_END
    pop $temp

    push_summary
sensors_END:
    return 0


