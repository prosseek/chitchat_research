# correlation producePrice = (priceMatch(produceName, price))
# function bool priceMatch(produceName, price) = {
#  return ( produceName == "apple" && price >=0 && price <= 1000 )
# }

# first
    read producename
    jpeekfalse END
    read price_i
    jpeekfalse END
    function_call_stack priceMatch 2
END:
    stop

priceMatch:
    load $bp - 2
    push "apple"
    cmp

    load $bp - 1
    push 0
    geq

    and

    load $bp - 1
    push 1000
    leq

    and
    return 2