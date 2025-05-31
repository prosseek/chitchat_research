# This is a test
    push 10
    push 20
    add
    push 30
    cmp
    jnz LABEL
    print "Same"
    jmp LAST
LABEL:
    jmpc LABEL2
LAST:
    stop
