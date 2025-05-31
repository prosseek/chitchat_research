#include <string>
#include <iostream>
#include <vector>

#include "util.h"
#include "serializerUtils.h"

using namespace std;

class Serializer {
protected:
    int bufferPointer = 0;
    vector<unsigned char> result;
    string tempResultInString;
    
    vector<unsigned char> intToByteArray(int value);
    int byteArrayToInt(const vector<unsigned char>& value);
    string byteArrayToString(const vector<unsigned char>& value); // , string str);
    time_t byteArrayToTimestamp(const vector<unsigned char>& value);
    vector<unsigned char> timestampToByteArray(time_t value);
public:
    Serializer() {}
    
    Serializer(const std::string& result)
    {
        Util::stringToByteArray(result, this->result);
    }

    Serializer(const vector<unsigned char>& result)
    {
        this->result = result;
    }
    
    // reset result and bufferPointer
    void setResult(const vector<unsigned char>& result)
    {
        this->result = result;
        bufferPointer = 0; 
    }
    
    void setResult(const std::string& result)
    {
        vector<unsigned char> res;
        Util::stringToByteArray(result, res);
        setResult(res);
    }
    
    vector<unsigned char> const& getResult() const
    {
        return this->result;
    }
    
    string const& getResultAsString()
    {
        tempResultInString.clear();
        Util::byteArrayToString(this->result, tempResultInString);
        return tempResultInString;
    }
    
    string to_string()
    {
        string res;
        Util::byteArrayToString(this->result, res);
        return to_string(res);
    }
    
    string to_string(const string& value, bool hex = false)
    {
        string res;

        for (unsigned char i: value) {        
            string temp = hex ? "[" + Util::byteToHexString(i) + "]" : "[" + std::to_string(i) + "]";
            res += temp;
        }
        return res;
    }
    
    //template<typename T>
    void writeObjectData(int value) // , string typeName)
    {
        vector<unsigned char> temp;
        temp = intToByteArray(value);
        this->result.insert(this->result.end(), temp.begin(), temp.end());
    }
    
    void writeObjectData(unsigned char value) // , string typeName)
    {
        vector<unsigned char> temp {value};
        this->result.insert(this->result.end(), temp.begin(), temp.end());
    }
    
    void writeObjectData(string value)
    {
        int length = value.size();
        writeObjectData(length);
        
        vector<unsigned char> temp;
        Util::stringToByteArray(value, temp);

        this->result.insert(this->result.end(), temp.begin(), temp.end());
    }
    
    void writeObjectData(time_t value)
    {
        vector<unsigned char> temp;
        temp = timestampToByteArray(value);
        this->result.insert(this->result.end(), temp.begin(), temp.end());
    }
    
    void readObjectData(const vector<unsigned char>& buffer, int& result)
    {
        result = byteArrayToInt(buffer);
    }
    
    void readObjectData(const vector<unsigned char>& buffer, unsigned char& result)
    {
        result = buffer[0]; // (buffer);
    }
    
    void readObjectData(const vector<unsigned char>& buffer, string& result, int length)
    {
        // extract the size of string length encoded in 4 bytes
        // std::vector<unsigned char>  sub(&buffer[0], &buffer[4]);
        // int length = byteArrayToInt(sub);
        
        std::vector<unsigned char>  sub2(&buffer[0], &buffer[   length]);
        result = byteArrayToString(sub2);
    }
    
    void readObjectData(const vector<unsigned char>& buffer, time_t& result)
    {
        result = byteArrayToTimestamp(buffer);
    }
    
    void reset()
    {
        result.clear();
        resetBufferPointer();
    }
    
    void resetBufferPointer()
    {
        bufferPointer = 0;
    }

    int size()
    {
        return this->result.size();
    }
    
    // http://stackoverflow.com/questions/421573/best-way-to-extract-a-subvector-from-a-vector
    // vector<T>::const_iterator first = myVec.begin() + 100000;
    // vector<T>::const_iterator last = myVec.begin() + 101000;
    // vector<T> newVec(first, last);
    void autoReadObjectData(string& result)
    {
        // 1. read integer first
        int startPointer = bufferPointer;
        int endPointer = bufferPointer + sizeof(int);
        auto first = this->result.begin() + startPointer;
        auto last = this->result.begin() + endPointer;
        vector<unsigned char> unsignedCharBuffer(first, last);
        int length;
        readObjectData(unsignedCharBuffer, length);
        
        startPointer = endPointer;
        endPointer = startPointer + length;
        first = this->result.begin() + startPointer;
        last = this->result.begin() + endPointer;
        vector<unsigned char> unsignedCharBuffer2(first, last); 
        
        string value;
        readObjectData(unsignedCharBuffer2, value, length);
        result = value;
        bufferPointer = endPointer;
    }
    
    void autoReadObjectData(unsigned char& result)
    {
        unsigned char value;
        
        int startPointer = bufferPointer;
        int endPointer = bufferPointer + 1;
        auto first = this->result.begin() + startPointer;
        auto last = this->result.begin() + endPointer;
        
        vector<unsigned char> unsignedCharBuffer(first, last); 
        readObjectData(unsignedCharBuffer, value);
        result = value;
        bufferPointer = endPointer;
    }
    
    void autoReadObjectData(int& result) 
    {
        int value;
        
        int startPointer = bufferPointer;
        int endPointer = bufferPointer + sizeof(int);
        auto first = this->result.begin() + startPointer;
        auto last = this->result.begin() + endPointer;
        
        vector<unsigned char> unsignedCharBuffer(first, last); 
        readObjectData(unsignedCharBuffer, value);
        result = value;
        bufferPointer = endPointer;
    }
        
    void autoReadObjectData(time_t& result)
    {
        int value;
        
        int startPointer = bufferPointer;
        int endPointer = bufferPointer + sizeof(time_t);
        auto first = this->result.begin() + startPointer;
        auto last = this->result.begin() + endPointer;
        
        vector<unsigned char> unsignedCharBuffer(first, last); 
        readObjectData(unsignedCharBuffer, value);
        result = value;
        bufferPointer = endPointer;
    }
};