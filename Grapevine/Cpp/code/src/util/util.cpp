//
// Created by smcho on 5/30/13.
// Copyright (c) 2013 ___MPC___. All rights reserved.
//
// To change the template use AppCode | Preferences | File Templates.
//
#include <algorithm>
#include "util.h"
//namespace bloomier {

/**
 * add all elements from bList into aList. aList will augment if bList has the elements that aList doesn't have.
 */ 
template <class T>
void Util::addAll(std::vector<T>& aList, const std::vector<T> bList)
{
    // copy all the elements in bList list into aList
    for (auto it = bList.begin(); it != bList.end(); ++it)
    {
        aList.push_back(*it);
    }
}
// specialization
template void Util::addAll<std::string>(std::vector<std::string>&, const std::vector<std::string>);
template void Util::addAll<int>(std::vector<int>&, const std::vector<int>);

/**
 * remove from aMap when bList has the corresponding key string. 
 * aMap = {'a':10, 'b':20}, bList = ['a'] => amMap = {'b':20} 'a' will be removed as the key is in bList
 */
template <class T1, class T2, class T3>
void Util::removeAll(std::map<T1, T2>& aMap, const std::vector<T3> bList)
{
    std::list<T1> keys;
    // 1. get all the keys that has the elements from bList
    for (auto it = bList.begin(); it != bList.end(); ++it)
    {
        for (auto j = aMap.begin(); j != aMap.end(); ++j)
        {
            if (j->first == *it) keys.push_back(j->first);
        }
    }
    // 2. remove all the items of the key
    for (auto it = keys.begin(); it != keys.end(); ++it)
    {
        aMap.erase(*it);
    }
}
template void Util::removeAll(std::map<std::string, int>& , const std::vector<std::string>);


template <class T>
void Util::removeAll(std::vector<T>& v1, const std::vector<T>& v2)
{
    std::list<T> containedValue;
    for (auto value : v1)
    {
        if (in(v2, value))
        {
            containedValue.push_back(value);
        }
    }
    
//  std::vector<int>::iterator
    for (auto value : containedValue)
    {
        typename std::vector<T>::iterator ip = find(v1.begin(), v1.end(), value);
        v1.erase(ip);
    }
    
}

template void Util::removeAll(std::vector<int>&, const std::vector<int>&);

/**
 * byteArrayXor does xor operation on byte (unsigned char) basis up up size.
 * result = ['0xFF', '0x00', '0xFF'], input = ['0xFF', '0xFF', '0xFF'], size = 3 =>
 * result = ['0x00', '0xFF', '0x00'] for 3 elements in result and input, the xor operation is executed 
 * to make result store the results
 */
void Util::byteArrayXor(unsigned char* result, const unsigned char* input, int size)
{
    //int size = std::min(sizeof(result)/sizeof(unsigned char), sizeof(input)/sizeof(unsigned char));

    for (int i = 0; i < size; i++)
    {
        result[i] = result[i] ^ input[i];
    }
}

/**
 * setInArray updates the contents in result from input up to size
 */
void Util::setInArray(unsigned char* result, const unsigned char* input, int size)
{
    for (int i = 0; i < size; i++)
    {
        result[i] = input[i]; // ^ input[i];
    }
}

/**
 * getByteSize returns the number of bytes from value
 * value:8 => 1 byte
 * value:10 => 2 bytes
 * value:32 => 32/8 = 4 bytes
 */
int Util::getByteSize(int value)
{
    // return q//8 + (1 if q % 8 != 0 else 0
    return value / 8 + (value % 8 == 0 ? 0 : 1);
}

/**
 *  in is an emulation of in operator in Python, the setArray should be set.
 *  in(set([10,20,30]), 20) => true, 20 in set([10,20,30])
 */
bool Util::in(std::set<int> setArray, int value)
{
    auto it = setArray.find(value);
    if (it == setArray.end()) // not found
        return false;
    else
        return true;
}

/**
 *  in is an emulation of in operator in Python, the setArray should be vector.
 *  in([10,20,30], 20) => true, 20 in set([10,20,30])
 */
template <class T>
bool Util::in(std::vector<T> vectorArray, T value)
{
    auto it = find(vectorArray.begin(), vectorArray.end(), value);
    if (it == vectorArray.end()) return false;
    return true;
}
template bool Util::in(std::vector<int> vectorArray, int value);
template bool Util::in(std::vector<std::string> vectorArray, std::string value);

// template <class T> 
// bool Util::in(std::map<int, std::unique_ptr<T>> m, int value)
// {
//     
// }
// template bool Util::in(std::map<int, std::unique_ptr<ContextSummary>> m, int value);

/**
 * emulation of copy.deepcopy() from python. 
 */
void Util::deepcopy(const std::map<std::string, int> source, std::map<std::string, int>& dest)
{
    for (auto it = source.begin(); it != source.end(); ++it)
    {
        //std::cout << it->first << ":" << it->second << std::endl;
        dest[it->first] = it->second;
    }
}

// template <class T>
// std::vector<T> Util::getKeys(std::map<T, int>& map)
// {
//     std::vector<std::string> result;
// 
//     for(auto key: map)
//         result.push_back(key.first);
//     return result;
// }
// template std::vector<std::string> Util::getKeys(std::map<std::string, int>& map);

template<class T>
bool Util::sameTwoVectors(std::vector<T> first, std::vector<T> second)
{
    sort (first.begin(), first.begin() + first.size());
    sort (second.begin(), second.begin() + second.size());
    return (first == second);
    //return true;
}
//template void Util::addAll<std::string>(std::vector<std::string>&, const std::vector<std::string>);
template bool Util::sameTwoVectors(std::vector<int> first, std::vector<int> second);
template bool Util::sameTwoVectors(std::vector<std::string> first, std::vector<std::string> second);

/*
 * DEBUGGING FUNCTIONS : print
 */
template <class T>
void Util::print(const std::vector<T>* vectorArray)
{
    for (auto i = vectorArray->begin(); i != vectorArray->end(); ++i)
    {
        std::cout << *i << ":";
    }
    std::cout << std::endl;
}

template <>
void Util::print(const std::vector<unsigned char>& vectorArray)
{
    return Util::printByteStream(vectorArray);
}

void Util::printByteStream(const std::vector<unsigned char>& input)
{
    for (auto val : input) printf("\\x%.2x", val);
    printf("\n");
}

template <class T>
void Util::print(const std::vector<T>& vectorArray)
{
    return Util::print(&vectorArray);
}

template void Util::print(const std::vector<int>* vectorArray);
template void Util::print(const std::vector<std::string>* vectorArray);
template void Util::print(const std::vector<int>& vectorArray);
template void Util::print(const std::vector<std::string>& vectorArray);

template <class T>
void Util::print(T* array, int size)
{
    std::cout << "ARRAY PRINT:" << size << "<";
    for (int i = 0; i < size; i++)
    {
        std::cout << int(array[i]) << ":";
    }
    std::cout << std::endl;
}
template void Util::print(int* vectorArray, int);
//template void Util::print(std::string* vectorArray, int);
template void Util::print(unsigned char* vectorArray, int);

bool Util::startswith(std::string mainstring, std::string substring)
{
    int mainlength = mainstring.size();
    int length = substring.size();
    if (length > mainlength) return false;
    
    std::string sub = mainstring.substr(0, length);
    return (sub == substring);
}
bool Util::endswith(std::string mainstring, std::string substring)
{
    int mainlength = mainstring.size();
    int length = substring.size();
    if (length > mainlength) return false;
    
    std::string sub = mainstring.substr(mainlength - length, mainlength);
    return (sub == substring);
}

template<typename T>
void Util::andOperation(const std::vector<T>& vectorArray1, const std::vector<T>& vectorArray2, std::vector<T>& result)
{
    for (auto element : vectorArray1)
    {
        if (Util::in(vectorArray2, element))
        {
            result.push_back(element);
        }
    }
}
template void Util::andOperation(const std::vector<int>& vectorArray1, const std::vector<int>& vectorArray2, std::vector<int>& result);

std::string Util::byteToHexString(unsigned char value)
{
    std::ostringstream oss;
    
    oss << std::hex << std::setw(2) << std::setfill('0') << int(value);
    return "0x" + oss.str();
}

void Util::byteArrayToString(const std::vector<unsigned char>& byteArray, std::string& result)
{
    for (auto elem : byteArray)
    {
        result += elem;
    }
}

void Util::stringToByteArray(const std::string str, std::vector<unsigned char>& result)
{
    for (auto elem : str)
    {
        result.push_back(elem);
    }
}

//} // namespace