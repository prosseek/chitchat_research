# This is for demonstration purposes not working code
# The compiler generates the assembly code shown

# -schema datetime = (date, time)
# -schema location = (longitude, latitude)
# -schema event = event | advertisement
# -schema sender = (name, id?) | "gchat id"
# +schema buyQuery = (sender, event, datetime, location)

# - schema datetime
# (a, b) => should use this template
#
DATETIME:
    f _READ_TO_REG date
    jfalsepeek DATETIME_END
    pop $temp

    f _READ_TO_REG time
    jfalsepeek DATETIME_END
    pop $temp

    push true
DATETIME_END:
    return 0

# event = event | advertisement
EVENT:
    f _READ_TO_REG_OR event advertisement 2
    jfalsepeek EVENT_END
    pop $temp
EVENT_END:
    return 0

# inner function from (...)
# -schema sender = (name, id?) | "gchat id"
SENDER_1:
# (name, id?)
    f _READ_TO_REG name
    jfalsepeek EVENT_END
    pop $temp

    f _READ_TO_REG_OPTION id
    jfalsepeek EVENT_END
    pop $temp
SENDER_1_END:
    return 0

SENDER:
    f _READ_TO_REG_OR SENDER_1 "gchat id" 2
    jfalsepeek EVENT_END
    pop $temp
EVENT_END:
    return 0

# +schema buyQuery = (sender, event, datetime, location)
buyQuery:
    f _READ_TO_REG_OR_FUNCTION SENDER
    ...