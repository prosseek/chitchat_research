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

_READ_TO_REG_OR_FUNCTION_CALL:
    load $bp - 1
    dup
    isstring
    jtrue _CALL_READ_TO_REG
    # $temp is function (number)
    pop $temp
    f $temp
    jmp _READ_TO_REG_OR_FUNCTION_CALL_END
_CALL_READ_TO_REG:
    pop $temp
    f _READ_TO_REG $temp
_READ_TO_REG_OR_FUNCTION_CALL_END:
    return 1

_READ_TO_REG_OR:
    # store local variable
    # i == bp + 2 -> first local variable
    push 0

    # the number of items
    load $bp - 1
    pop $count

    # bp - ($count + 1) 1st element
    # bp - ($count + 1 - 1) 2nd element
    # bp - ($count + 1 - 2) 3rd element
    # or (bp - 2 - 0) -> last element     or (bp - 1 - 1)
    #    (bo - 2 - 1) -> last -1 element  or (bp - 1 - 2)
    #                    last element is (bp - 1 - $count)

    # i (bp + 2) <- 0
    push 0
    store $bp + 2

_READ_TO_REG_OR_LOOP:
    # check i == $count
    load $bp + 2
    push $count
    cmp
    # if different execute again
    jtrue _READ_TO_REG_OR_END_NO_RESULT

    # get ith parameter, run it, i <- i+1 and goto loop start
    # -(2 + i) => $bp - (2 + i)
    push 2
    load $bp + 2
    iadd
    pop $temp

    # get parameter
    load $bp - $temp
    pop $temp
    f _READ_TO_REG_OR_FUNCTION_CALL $temp
    jpeektrue _READ_TO_REG_OR_END
    # try again as the label is not in the summary
    # i += 1
    load $bp + 2
    push 1
    iadd
    store $bp + 2
    # remove the previous result
    pop $temp
    jmp _READ_TO_REG_OR_LOOP

_READ_TO_REG_OR_END_NO_RESULT:
    push false
_READ_TO_REG_OR_END:
    swap
    # pop off the local variable
    pop $temp

    # remove total number of parameter (count + 1)
    #load $bp - 1
    push $count
    push 1
    iadd
    pop  $temp
    return $temp

_READ_OPTION:
    load $bp - 1
    pop $temp
    f _READ_TO_REG $temp
    pop $temp
    # always return true
    push true
    return 1

SENSOR_1:
    f _READ_TO_REG a
    jpeekfalse SENSOR_1_END
    pop $temp

    f _READ_OPTION b
    jpeekfalse SENSOR_1_END
    pop $temp

    push true
SENSOR_1_END:   
    return 0

## START
# +schema sensors = (a, b?) | c
# (a, b?) should be compiled as a function
START:
    function_call SENSORS
    stop

SENSORS:
    f _READ_TO_REG_OR SENSOR_1 c 2

    jpeekfalse SENSORS_END
    pop $temp

# final - summing up the summary
    push_summary
SENSORS_END:
    return 0
