//
// Created by smcho on 5/30/13.
// Copyright (c) 2013 ___MPC___. All rights reserved.
//
// To change the template use AppCode | Preferences | File Templates.
//



#ifndef __SERIALIZER_UtilS_H_
#define __SERIALIZER_UtilS_H_

#include <iostream>
#include <list>
#include <set>
#include <algorithm>
#include <vector>
#include <map>
#include <string>
#include <ctime>

class SerializerUtils {
    template <typename T>
    static std::vector<unsigned char> valueToByteArray(T value); // , int size);
    template <typename T>
    static T byteArrayToValue(std::vector<unsigned char> value); // , int size);
public:
    static std::vector<unsigned char> intToByteArray(int value);
    static std::vector<unsigned char> timestampToByteArray(time_t timestamp);
    static int byteArrayToInt(const std::vector<unsigned char>& value);
    static time_t byteArrayToTime(const std::vector<unsigned char>& value);
};
//}

#endif
