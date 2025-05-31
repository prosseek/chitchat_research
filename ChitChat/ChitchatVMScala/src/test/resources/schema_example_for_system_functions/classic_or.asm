# +schema sensors = (name , event | advertisement)
# startup code
    jmp START

# for a
_READ_TO_REG:
    load $bp - 1
    pop $temp
    read $temp
    jpeekfalse _READ_TO_REG_END
    register $temp
    push true
_READ_TO_REG_END:
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
    f _READ_TO_REG $temp
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

    # a | b | c | d
    f _READ_TO_REG_OR d c b a 4
    jpeekfalse SENSORS_END
    pop $temp

# final - summing up the summary
    push_summary
SENSORS_END:
    return 0
