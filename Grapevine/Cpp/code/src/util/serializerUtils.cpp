#include "serializerUtils.h"

template <typename T>
std::vector<unsigned char> SerializerUtils::valueToByteArray(T value) // , int size)
{
    std::vector<unsigned char> result;
    int length = sizeof(T);
    
    for (int i = length - 1; i >= 0; i--) {
        result.push_back(value >> i*8);
    }
    return result;
}

template <typename T>
T SerializerUtils::byteArrayToValue(std::vector<unsigned char> value)
{
    T result = 0;
    int length = value.size();
    for (int i = 0; i < length; i++)
    {
        // big endian
        unsigned char temp = value[i];
        result += ((T) temp)*(1 << 8*(length - 1 - i));
    }
    return result;
} 
//template std::vector<unsigned char> SerializerUtils::valueToByteArray(int value);

std::vector<unsigned char> SerializerUtils::intToByteArray(int value)
{
    return valueToByteArray<int>(value);
}

std::vector<unsigned char> SerializerUtils::timestampToByteArray(time_t value)
{
    return valueToByteArray<time_t>(value);
}

int SerializerUtils::byteArrayToInt(const std::vector<unsigned char>& value)
{
    return byteArrayToValue<int>(value);
}
time_t SerializerUtils::byteArrayToTime(const std::vector<unsigned char>& value)
{
    return byteArrayToValue<time_t>(value);
}