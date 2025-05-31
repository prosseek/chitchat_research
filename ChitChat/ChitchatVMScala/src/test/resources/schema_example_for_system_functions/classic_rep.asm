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

# if given _CHECK_LABELS a b 0 2
# the last 2 means there are two labels (a/b)        
# checks if a0 b0 is in the summary
_CHECK_LABELS:
    # reserve variable
    push 0

    # the number of items
    load $bp - 1
    pop $count
        
_CHECK_LABELS_LOOP:
    # check i == $count
    load $bp + 2
    push $count
    cmp

    # everything was OK so return
    jtrue _CHECK_LABELS_END_OK

    # get ith parameter, run it, i <- i+1 and goto loop start
    # -(3 + i) => $bp - (3 + i)
    push 3
    load $bp + 2
    iadd
    pop $temp

    # get parameter
    load $bp - $temp
    # get appended to the parameter from input parameter (bp -2)
    # to make a 2 => a2
    load $bp - 2
    concat

    pop $temp

    f _READ_TO_REG $temp
    jpeekfalse _CHECK_LABELS_END

    # try again as the label is not in the summary
    # i += 1
    load $bp + 2
    push 1
    iadd
    store $bp + 2
    # remove the previous result
    pop $temp
    jmp _CHECK_LABELS_LOOP

_CHECK_LABELS_END_OK:
    push true
        
_CHECK_LABELS_END:
    swap
    # pop off the local variable
    pop $temp

    # remove total number of parameter (count + 2)
    #load $bp - 1
    push $count
    push 2
    iadd
    pop  $temp
    return $temp

_READ_TO_REG_REP:
    # reserve variable at i ($bp + 2) 
    push 0
    # reserve another variable at result ($bp + 3)
    push false
    # reserve the index to concatenate to label ($bp + 4)
    push 0

    # the number of items
    load $bp - 1
    pop $count

_RESET_I_AND_START_PUSH_PARAM:
    # as the next step is to add 1, we should start from -1
    push -1
    store $bp + 2    
        
    # 1. push all the parameters
_PUSH_PARAMS_LOOP:
    # i += 1
    load $bp + 2
    push 1
    iadd
    store $bp + 2

    # check i == $count
    load $bp + 2
    push $count
    cmp

    jtrue _PUSH_PARAMS_LOOP_END

    # get the param which is in bp - (2 + i)
    # push i    
    push 2
    load $bp + 2
    iadd
    pop $temp
    load $bp - $temp
        
    jmp _PUSH_PARAMS_LOOP

_PUSH_PARAMS_LOOP_END:
    # two more parameters other than labels
    # 1. index (to attach to label)
    # 2. total number
    load $bp + 4
    push $count

    # increase the index by 1
    load $bp + 4
    push 1
    iadd
    store $bp + 4

    # the total parameter is $count + 2 (the count itself)
    push $count
    push 2
    iadd
    pop $temp

    # 2. function call
    function_call_stack _CHECK_LABELS $temp
    jpeekfalse _READ_TO_REG_LOOP_END

    # set the result as true
    store $bp + 3
    jmp _RESET_I_AND_START_PUSH_PARAM
        
_READ_TO_REG_LOOP_END:
    # rv <- result
    # 1. pop the tos
    # 2. pop off three local variables    
    # 3. store $bp + 3 (result) to tos
    pop $temp
    # i    
    pop $temp
    # result
    pop $temp2
    # index
    pop $temp

    # push back the result
    push $temp2
        
    # remove total number of parameter (count + 1)
    #load $bp - 1
    push $count
    push 1
    iadd
    pop  $temp
    return $temp
        
## START
# +schema sensors = ((sensor, value)+ )

START:
    function_call SENSORS
    stop

SENSORS:
    # 0 -> sensor0/value0
    # 2 -> there are two elements
    f _READ_TO_REG_REP sensor value 2
    jpeekfalse SENSORS_END
    pop $temp
# final - summing up the summary
    push_summary
SENSORS_END:
    return 0
