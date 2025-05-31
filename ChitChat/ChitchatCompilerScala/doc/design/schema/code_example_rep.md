## Example Input
`# + schema x = (name , event , (sensor, value)+ )`

### Idea

1. Repetition becomes additional function call.
2. The function call is ATN state machine transition code.

```
    f ITER
    jpeekfalse END
    pop $temp
```
3. We need labels.
    1. function name => `f + "_REP" (ITER in example)`
    2. start loop => `f + "_START" (START in example)`
    2. end for error => `f + "_ERROREND" (ERRORENDLOOP in example)`
    3. end for loop  => `f + "_LOOPEND" (ENDLOOP in example)`

### ATN transition code

#### Reserve one local variables. (i)

```
    # i = 0
    # one local variable
    # i == bp + 2 -> first variable
    push 0

    # assignment i = 0
    push 0
    store $bp + 2
```

#### Read the variables at least one time

```
    # there should be at least one sensor data
    load $bp + 2
    pop $temp
    <<<
    read sensor $temp
    jpeekfalse ERRORENDLOOP
    register sensor $temp
    >>>
    <<<
    read value $temp
    jpeekfalse ERRORENDLOOP
    register value $temp
    >>>

```

#### Iteration to get values

```
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

    <<<
    read sensor $temp
    jpeekfalse ENDLOOP
    register sensor $temp
    >>>

    <<<
    read value $temp
    jpeekfalse ENDLOOP
    register value $temp
    >>>

    jmp START
```

#### Finalise and return
```
ERRORENDLOOP:
    # false - local_variable - ... (before in stack)
    # local_variable - false - ... (after in stack)
    swap
ENDLOOP:
    # remove a local variable
    pop
    r 0
```

### Example output

```
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
    
ITER:
    push 0
    push 0
    store $bp + 2
    load $bp + 2
    pop $temp
    read sensor $temp
    jpeekfalse ERRORENDLOOP
    register sensor $temp
    read value $temp
    jpeekfalse ERRORENDLOOP
    register value $temp
START:
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
    swap
ENDLOOP:
    pop
    r 0
```