# This is a test
    push 10
    push 20
LABEL:
    add
    jmp LABEL
LABEL2:
    jmpc LABEL2
    stop
