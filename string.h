#include <cstring>
#include <iostream>

class String {
  char* string_ = nullptr;
  size_t size_ = 0;
  size_t capacity_ = 1;
 public:
  String() {}
  String(size_t count) : string_(new char[count + 1]), size_(count), capacity_(count + 1) {}
  String(size_t count, char symb) : String(count) {
    memset(string_, symb, count);
    string_[size_] = '\0';
  }
  String(const char* str) : String(strlen(str), '0') {
    memcpy(string_, str, size_);
    string_[size_] = '\0';
  }
  String(const String& other) : string_(new char[other.capacity_]), size_(other.size_), capacity_(other.capacity_) {
    memcpy(string_, other.string_, size_);
    string_[size_] = '\0';
  }
  String(char element) : String(1, element) {}

  ~String() {
    delete[] string_;
  }

  char& operator[](int index) {
    return string_[index];
  }
  const char& operator[](int index) const {
    return string_[index];
  }

  size_t length() const {
    return size_;
  }

  size_t size() const {
    return size_;
  }

  size_t capacity() const {
    return capacity_ - 1;
  }

  void push_back(const char element) {
    if (capacity_ - 1 == size_) {
      capacity_ *= 2;
      string_ = (char*)realloc(string_, sizeof(char) * capacity_);
    }
    string_[size_] = element;
    ++size_;
    string_[size_] = '\0';
  }

  void pop_back() {
    --size_;
    string_[size_] = '\0';
  }

  char& front() {
    return string_[0];
  }

  char& back() {
    return string_[size_ - 1];
  }

  const char& front() const {
    return string_[0];
  }

  const char& back() const {
    return string_[size_ - 1];
  }

  size_t universal_find(const String& substring, size_t first, size_t second) const {
    for (size_t i = 0; i < size_ - substring.size_ + 1; ++i) {
      bool flag = true;
      for (size_t j = 0; j < substring.size_; ++j) {
        if (string_[(size_ - 1) * first + (i + j) * second] != substring.string_[(substring.size_ - 1) * first + j * second]) {
          flag = false;
          break;
        }
      }
      if (flag) {
        return (size_ - 1) * first + i * second - first * (substring.size_ - 1);
      }
    }
    return size_;
  }

  size_t find(const String& substring) const {
    return universal_find(substring, 0, 1);
  }

  size_t rfind(const String& substring) const {
    return universal_find(substring, 1, -1);
  }

  String substr(size_t start, size_t count) const {
    String substring(count);
    for (size_t i = start; i < start + count; ++i) {
      substring.string_[i - start] = string_[i];
    }
    substring.string_[count] = '\0';
    return substring;
  }

  bool empty() const {
    return size_ == 0;
  }

  void clear() {
    string_[0] = '\0';
    size_ = 0;
  }

  void shrink_to_fit() {
    string_ = (char*)realloc(string_, sizeof(char) * (size_ + 1));
    capacity_ = size_ + 1;
  }

  char* data() const {
    return string_;
  }

  String& operator+=(const String& second) {
    if (size_ + second.size_ > size_) {
      string_ = (char*) realloc(string_, sizeof(char) * (size_ + second.size_ + 1));
    }
    for (size_t i = 0; i < second.size_; ++i) {
      string_[size_ + i] = second.string_[i];
    }
    size_ += second.size_;
    capacity_ = size_ + 1;
    string_[size_] = '\0';
    return *this;
  }

  String& operator=(const String& different) {
    if (string_ == different.string_) {
      return *this;
    }
    string_ = (char*)realloc(string_, sizeof(char) * (different.size_ + 1));
    for (size_t i = 0; i < different.size_; ++i) {
      string_[i] = different.string_[i];
    }
    size_ = different.size_;
    capacity_ = size_ + 1;
    string_[size_] = '\0';
    return *this;
  }
};

bool operator==(const String& first, const String& second) {
  if (strcmp(first.data(), second.data()) == 0) {
    return true;
  }
  return false;
}

bool operator<(const String& first, const String& second) {
  for (size_t i = 0; i < std::min(first.size(), second.size()); ++i) {
    if (first.data()[i] < second.data()[i]) {
      return true;
    } else if (first.data()[i] > second.data()[i]) {
      return false;
    }
  }
  return first.size() < second.size();
}

bool operator>(const String& first, const String& second) {
  return second < first;
}

bool operator<=(const String& first, const String& second) {
  return !(first > second);
}

bool operator>=(const String& first, const String& second) {
  return !(first < second);
}

bool operator!=(const String& first, const String& second) {
  return !(first == second);
}

String operator+(const String& first, const String& second) {
  String result(first);
  result += second;
  return result;
}

std::ostream& operator << (std::ostream& output_stream, const String& str) {
  output_stream << str.data();
  return output_stream;
}

std::istream& operator >> (std::istream& input_stream, String& str) {
  char current_char;

  while (input_stream.get(current_char)) {
    if (isspace(current_char)) {
      break;
    }
    str.push_back(current_char);
  }
  return input_stream;
}
