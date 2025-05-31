# value cityParkCenter(latitude, longitude) = { ...
# situation nearCityPark() = |(latitude, longitude) - cityParkCenter| <= 5 _km
    f2 nearCityPark 0
END:
    stop

nearCityPark:
    read latitude
    jpeekfalse END
    read longitude
    jpeekfalse END
    push [30, 25, 1, 74]
    push [-97, 47, 21, 83]
    abs location
    push 5000.0
    fleq
    r 0
