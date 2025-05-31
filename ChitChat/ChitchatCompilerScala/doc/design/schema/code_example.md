## Example

`+schema sensors = (name , event | advertisement , time?)`

### Idea

1. The schema call becomes a function call.
2. There are four possibilities, provide the code generator for each case.
   1. only name
   2. choice
   3. optional
   4. repetition (explained in code_example_rep document)
3. When all is done, `push_summary` and return.

```
   function_call SENSORS
   stop

   ...

       push_summary
   END:
       return 0

```

### Only name

In the example, `name` is translated as follows. We need to creat an unique END label.

```
    read name
    jpeekfalse END
    register name
```

### Choice

Choice requires two additional labels (normal, end label).

```
# event | advertisement
    read event
    jpeekfalse ADVERTISEMENT
    register event
    jmp ADVERTISEMENTEND
ADVERTISEMENT:
    pop $temp
    read advertisement
    jpeekfalse END
    register advertisement
ADVERTISEMENTEND:
```

### Optional

Optional also requires two additional label. No end label is needed.

```
# time?
    read time
    jpeekfalse TIMEEND
    register time
    jmp TIMENEXT
TIMEEND:
    pop $temp
TIMENEXT:
```

### Overall results

```
    function_call SENSORS
    stop

SENSORS:
    read name
    jpeekfalse END
    register name

# event | advertisement
    read event
    jpeekfalse ADVERTISEMENT
    register event
    jmp ADVERTISEMENTEND
ADVERTISEMENT:
    pop $temp
    read advertisement
    jpeekfalse END
    register advertisement
ADVERTISEMENTEND:

# time?
    read time
    jpeekfalse TIMEEND
    register time
    jmp TIMENEXT
TIMEEND:
    pop $temp
TIMENEXT:

# final - summing up the summary
    push_summary
END:
    return 0
```