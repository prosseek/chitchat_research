# (a b c)
    read a
    jpeekfalse END
    register a
    read b
    jpeekfalse END
    register b
    read c
    jpeekfalse END
    register c
    push_summary
END:
    stop
