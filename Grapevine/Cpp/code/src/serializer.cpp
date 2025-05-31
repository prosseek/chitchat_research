#include "serializer.h"

std::vector<unsigned char> Serializer::intToByteArray(int value)
{
    return SerializerUtils::intToByteArray(value);
}

int Serializer::byteArrayToInt(const vector<unsigned char>& value)
{
    return SerializerUtils::byteArrayToInt(value);
}

time_t Serializer::byteArrayToTimestamp(const vector<unsigned char>& value)
{
    return SerializerUtils::byteArrayToTime(value);
}

string Serializer::byteArrayToString(const vector<unsigned char>& value) // , string str)
{
    tempResultInString.clear();
    Util::byteArrayToString(value, tempResultInString);
    return tempResultInString;
}

std::vector<unsigned char> Serializer::timestampToByteArray(time_t value)
{
    return SerializerUtils::timestampToByteArray(value);
}