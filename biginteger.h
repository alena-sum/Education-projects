#include <algorithm>
#include <iostream>
#include <math.h>
#include <string>
#include <vector>

class BigInteger {
  const long long kImportantNum = 1e9;
  const int kLen = 9;

  std::vector<long long> ranks;
  bool sign = false;

  BigInteger(std::string str) {
    int st_index = 0;
    if (str[0] == '-') {
      ++st_index;
      sign = true;
    }
    int sz = (int)str.size();
    for (int i = sz - 1; i >= st_index; i -= kLen) {
      int cur_num = 0;
      int factor = 1;
      int end = i - kLen;
      if (st_index - 1 > end) {
        end = st_index - 1;
      }
      for (int j = i; j > end; --j) {
        cur_num += factor * (str[j] - '0');
        factor *= 10;
      }
      ranks.push_back(cur_num);
    }
  }
 public:
  BigInteger() {}
  BigInteger(int number) {
    sign = number < 0;
    if (number == 0) {
      ranks.push_back(0);
    }
    while (number) {
      ranks.push_back(abs(number % kImportantNum));
      number /= kImportantNum;
    }
  }
  BigInteger(std::vector<long long> ranks, bool sign) : ranks(ranks), sign(sign) {}
  explicit BigInteger(unsigned long long number) {
    while (number) {
      ranks.push_back(abs((long long)(number % kImportantNum)));
      number /= kImportantNum;
    }
  }

  BigInteger operator-() const {
    if (ranks.size() > 1 || (ranks[0] != 0 && ranks.size() == 1)) {
      return BigInteger(ranks, !sign);
    }
    return BigInteger(ranks, false);
  }
  BigInteger& operator=(const BigInteger& another) {
    ranks = another.ranks;
    sign = another.sign;
    return *this;
  }
  BigInteger& operator+=(const BigInteger& another_num) {
    BigInteger another(another_num);
    if (sign == another.sign) {
      if (another.ranks.size() > ranks.size()) {
        ranks.resize(another.ranks.size());
      } else {
        another.ranks.resize(ranks.size());
      }
      long long cur_result = 0;
      for (int i = 0; i < (int)ranks.size(); ++i) {
        cur_result += ranks[i] + another.ranks[i];
        if (cur_result >= kImportantNum) {
          ranks[i] = cur_result % kImportantNum;
          cur_result /= kImportantNum;
        } else {
          ranks[i] = cur_result;
          cur_result = 0;
        }
      }
      if (cur_result != 0) {
        ranks.push_back(cur_result);
      }
      return *this;
    }

    long long indicator = -1;
    if (ranks.size() > another.ranks.size()) {
      indicator *= -1;
    } else if (ranks.size() < another.ranks.size()) {
      sign = another.sign;
    } else {
      sign = false;
      for (int i = (int)ranks.size() - 1; i >= 0; --i) {
        if (ranks[i] > another.ranks[i]) {
          sign = !another.sign;
          indicator *= -1;
          break;
        }
        if (ranks[i] < another.ranks[i]) {
          sign = another.sign;
          break;
        }
      }
    }
    if (another.ranks.size() > ranks.size()) {
      ranks.resize(another.ranks.size());
    } else {
      another.ranks.resize(ranks.size());
    }
    long long cur_result;
    for (int i = 0; i < (int)ranks.size(); ++i) {
      cur_result = (ranks[i] - another.ranks[i]) * indicator;
      if (cur_result >= 0) {
        ranks[i] = cur_result;
      } else {
        cur_result += kImportantNum;
        ranks[i] = cur_result;
        if (indicator == -1) {
          --another.ranks[i + 1];
        } else {
          --ranks[i + 1];
        }
      }
    }
    while (ranks.back() == 0 && ranks.size() > 1) {
      ranks.pop_back();
    }
    return *this;
  }
  BigInteger& operator-=(const BigInteger& another) {
    *this += -another;
    return *this;
  }
  BigInteger& operator*=(const BigInteger& another_num) {
    if ((another_num.ranks.size() == 1 && another_num.ranks[0] == 0) ||
        (ranks.size() == 1 && ranks[0] == 0)) {
      ranks.clear();
      ranks.push_back(0);
      sign = false;
      return *this;
    }
    sign = sign ^ another_num.sign;
    BigInteger this_num = *this;
    ranks.assign(this_num.ranks.size() + another_num.ranks.size() + 1, 0);
    long long cur_result;
    for (int i = 0; i < (int)another_num.ranks.size(); ++i) {
      for (int j = 0; j < (int)this_num.ranks.size(); ++j) {
        cur_result = another_num.ranks[i] * this_num.ranks[j] + ranks[i + j];
        ranks[i + j] = cur_result % kImportantNum;
        ranks[i + j + 1] += cur_result / kImportantNum;
      }
    }
    while (ranks.back() == 0 && ranks.size() > 1) {
      ranks.pop_back();
    }
    return *this;
  }
  BigInteger& operator/=(const BigInteger& another) {
    bool ans_sign = false;
    if (sign != another.sign) {
      ans_sign = true;
    }
    BigInteger del(another.ranks, false);
    std::vector<long long> answer;
    BigInteger cur_result = 0;
    for (int i = (int)ranks.size() - 1; i >= 0; --i) {
      cur_result *= kImportantNum;
      cur_result += ranks[i];
      long long start = -1;
      long long end = kImportantNum;
      BigInteger cur_del;
      while (end - start > 1) {
        long long middle = (start + end) / 2;
        cur_del = del;
        cur_del *= middle;
        if (cur_del <= cur_result) {
          start = middle;
        } else {
          end = middle;
        }
      }
      if (start == -1) {
        start = 0;
      }
      answer.push_back(start);
      cur_del = del;
      cur_del *= start;
      cur_result -= cur_del;
    }
    std::vector<long long> reverse_ans(answer.size());
    for (int i = 0; i < (int)reverse_ans.size(); ++i) {
      reverse_ans[i] = answer.back();
      answer.pop_back();
    }
    while (reverse_ans.back() == 0 && reverse_ans.size() > 1) {
      reverse_ans.pop_back();
    }
    if (reverse_ans.size() == 1 && reverse_ans[0] == 0) {
      ans_sign = false;
    }
    ranks = reverse_ans;
    sign = ans_sign;
    return *this;
  }
  BigInteger& operator%=(const BigInteger& another) {
    BigInteger temp(*this);
    temp /= another;
    temp *= another;
    *this -= temp;
    return *this;
  }
  BigInteger operator++(int) {
    BigInteger copy = *this;
    *this += 1;
    return copy;
  }
  BigInteger& operator++() {
    *this += 1;
    return *this;
  }
  BigInteger operator--(int) {
    BigInteger copy = *this;
    *this -= 1;
    return copy;
  }
  BigInteger& operator--() {
    *this -= 1;
    return *this;
  }

  std::string toString() const {
    std::string answer = "";
    if (sign) {
      answer.push_back('-');
    }
    for (int i = (int)ranks.size() - 1; i >= 0; --i) {
      long long cur_rank = ranks[i];
      std::string cur_string = std::to_string(cur_rank);
      if (i != (int)ranks.size() - 1) {
        while ((int)cur_string.size() < kLen) {
          cur_string = "0" + cur_string;
        }
      }
      answer += cur_string;
    }
    int count0 = 0;
    if (answer[0] == '-') {
      while (answer[count0 + 1] == 0) {
        ++count0;
      }
      answer = "-" + answer.substr(1 + count0, answer.size());
    } else {
      while (answer[count0] == 0) {
        ++count0;
      }
      answer = answer.substr(count0, answer.size());
    }
    return answer;
  }
  explicit operator bool() const {
    return !(ranks.size() == 1 && ranks[0] == 0);
  }

  friend bool operator<(const BigInteger& first, const BigInteger& second);
  friend bool operator==(const BigInteger& first, const BigInteger& second);
  friend bool operator<=(const BigInteger& first, const BigInteger& second);
  friend std::istream& operator>>(std::istream& input_stream, BigInteger& number);
  friend BigInteger operator""_bi(const char* number);

  ~BigInteger() = default;
};

bool operator<(const BigInteger& first, const BigInteger& second) {
  if (first.sign != second.sign || first.ranks.size() > second.ranks.size()) {
    return first.sign;
  }
  if (first.ranks.size() < second.ranks.size()) {
    return !second.sign;
  }
  bool answer = false;
  for (int i = (int)first.ranks.size() - 1; i >= 0; --i) {
    if (((second.ranks[i] < first.ranks[i]) == first.sign) && second.ranks[i] != first.ranks[i]) {
      answer = true;
      break;
    } else if (((second.ranks[i] > first.ranks[i]) == first.sign) && first.ranks[i] != second.ranks[i]) {
      break;
    }
  }
  return answer;
}
bool operator==(const BigInteger& first, const BigInteger& second) {
  if ((first.sign != second.sign) || (first.ranks.size() != second.ranks.size())) {
    return false;
  }
  bool answer = true;
  for (int i = 0; i < (int)first.ranks.size(); ++i) {
    if (first.ranks[i] != second.ranks[i]) {
      answer = false;
      break;
    }
  }
  return answer;
}
bool operator!=(const BigInteger& first, const BigInteger& second) {
  return !(first == second);
}
bool operator>(const BigInteger& first, const BigInteger& second) {
  return second < first;
}
bool operator<=(const BigInteger& first, const BigInteger& second) {
  return !(first > second);
}
bool operator>=(const BigInteger& first, const BigInteger& second) {
  return !(first < second);
}
BigInteger operator+(const BigInteger& first, const BigInteger& second) {
  BigInteger answer(first);
  answer += second;
  return answer;
}
BigInteger operator-(const BigInteger& first, const BigInteger& second) {
  BigInteger answer(first);
  answer -= second;
  return answer;
}
BigInteger operator*(const BigInteger& first, const BigInteger& second) {
  BigInteger answer(first);
  answer *= second;
  return answer;
}
BigInteger operator/(const BigInteger& first, const BigInteger& second) {
  BigInteger answer(first);
  answer /= second;
  return answer;
}
BigInteger operator%(const BigInteger& first, const BigInteger& second) {
  BigInteger answer(first);
  answer %= second;
  return answer;
}

std::ostream& operator<<(std::ostream& output_stream, const BigInteger& number) {
  output_stream << (number).toString();
  return output_stream;
}

std::istream& operator>>(std::istream& input_stream, BigInteger& number) {
  std::string string;
  input_stream >> string;
  BigInteger result{string};
  number = result;
  return input_stream;
}

BigInteger operator""_bi(unsigned long long number) {
  return BigInteger(number);
}

BigInteger operator""_bi(const char* number) {
  return BigInteger(number);
}


class Rational {
  size_t kNumber = 20;

  BigInteger numerator = 0;
  BigInteger denominator = 1;
  BigInteger Gcd (BigInteger first, BigInteger second) {
    if (second == 0) {
      return first;
    }
    return Gcd(second, first % second);
  }
  void MakeNotContractile() {
    BigInteger great_com_div = Gcd(numerator, denominator);
    numerator /= great_com_div;
    denominator /= great_com_div;
    if (denominator < 0) {
      numerator = -numerator;
      denominator = -denominator;
    }
  }
 public:
  Rational() {}
  Rational(BigInteger num) : numerator(num) {}
  Rational(int num) : Rational((BigInteger)num) {}
  Rational(BigInteger num, BigInteger den) : numerator(num), denominator(den) {
    MakeNotContractile();
  }
  Rational(int num, int den) : Rational((BigInteger)num, (BigInteger)den) {}

  Rational operator-() {
    numerator = -numerator;
    return *this;
  }
  Rational& operator+=(const Rational& another) {
    numerator = numerator * another.denominator + another.numerator * denominator;
    denominator *= another.denominator;
    MakeNotContractile();
    return *this;
  }
  Rational& operator-=(Rational another) {
    *this += -another;
    return *this;
  }
  Rational& operator*=(const Rational& another) {
    numerator *= another.numerator;
    denominator *= another.denominator;
    MakeNotContractile();
    return *this;
  }
  Rational& operator/=(const Rational& another) {
    numerator *= another.denominator;
    denominator *= another.numerator;
    MakeNotContractile();
    return *this;
  }

  std::string toString() const {
    if (denominator == 1) {
      return numerator.toString();
    }
    return numerator.toString() + "/" + denominator.toString();
  }
  std::string asDecimal(size_t precision = 0) const {
    BigInteger new_num = numerator;
    for (size_t i = 0; i < precision; ++i) {
      new_num *= 10;
    }
    std::string result = (new_num / denominator).toString();
    if ((result.size() <= precision && new_num >= 0) ||
        (result.size() - 1 <= precision && new_num < 0)) {
      if (new_num < 0) {
        result = result.substr(1, result.size());
      }
      int del = (int)precision - (int)result.size();
      for (int i = 0; i <= del; ++i) {
        result = "0" + result;
      }
      if (new_num < 0) {
        result = "-" + result;
      }
    }
    result.insert(result.end() - precision, '.');
    return result;
  }

  explicit operator double() const {
    return std::stod(asDecimal(kNumber));
  }

  friend bool operator<(const Rational& first, const Rational& second);
  friend bool operator==(const Rational& first, const Rational& second);

  ~Rational() = default;
};

bool operator<(const Rational& first, const Rational& second) {
  return (first.numerator * second.denominator < first.denominator * second.numerator);
}
bool operator==(const Rational& first, const Rational& second) {
  return (first.numerator == second.numerator && first.denominator == second.denominator);
}
bool operator>(const Rational& first, const Rational& second) {
  return second < first;
}
bool operator!=(const Rational& first, const Rational& second) {
  return !(first == second);
}
bool operator<=(const Rational& first, const Rational& second) {
  return !(first > second);
}
bool operator>=(const Rational& first, const Rational& second) {
  return !(first < second);
}

Rational operator+(const Rational& first, const Rational& second) {
  Rational answer(first);
  answer += second;
  return answer;
}
Rational operator-(const Rational& first, const Rational& second) {
  Rational answer(first);
  answer -= second;
  return answer;
}
Rational operator*(const Rational& first, const Rational& second) {
  Rational answer(first);
  answer *= second;
  return answer;
}
Rational operator/(const Rational& first, const Rational& second) {
  Rational answer(first);
  answer /= second;
  return answer;
}

