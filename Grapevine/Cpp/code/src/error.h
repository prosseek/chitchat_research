#ifndef __END_H__
#define __END_H__

#include <stdexcept>

class Error : public std::runtime_error
{
  public:
    Error (const std::string &message)
      : std::runtime_error(message)
    {}
};

#endif