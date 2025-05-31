# +schema sensors = (name , event | advertisement , time?)

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
