# situation partyTime(partyname) = ((date, time) - now) >= 0 _hour
# trigger: partyname, date, time

    read partyname
    jpeekfalse END
    f2 partyTime 0
END:
    stop

partyTime:
    read time
    jpeekfalse END
    read date
    jpeekfalse END
    here
    distance datetime
    push 0
    geq
    r 0
