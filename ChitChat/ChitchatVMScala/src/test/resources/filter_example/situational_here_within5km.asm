# situation within5km(market) = |here - (latitude, longitude)| <= 5 _km
    read market
    jmpnull END
    f2 within5km 1
END:
    stop
within5km:
    here
    read latitude
    jmpnull END
    read longitude
    jmpnull END
    abs location
    push 5000.0
    fleq
    r 0
