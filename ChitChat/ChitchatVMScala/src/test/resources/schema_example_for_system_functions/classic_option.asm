# +schema sensors = (name , time?)
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

_READ_OPTION:
    load $bp - 1
    pop $temp
    f _READ_TO_REG $temp
    pop $temp
    # always return true
    push true
    return 1

## START
# +schema sensors = (name , a | b | c | d)

START:
    function_call SENSORS
    stop

SENSORS:
    # name
    f _READ_TO_REG name
    jpeekfalse SENSORS_END
    pop $temp

    # time?
    f _READ_OPTION time
    jpeekfalse SENSORS_END
    pop $temp

# final - summing up the summary
    push_summary
SENSORS_END:
    return 0
