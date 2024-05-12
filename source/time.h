#include "consts.h"
#include <chrono>
#include <iostream>

#pragma once

class Time {
  long long initial_time;
  long long cur_time;

 public:
  Time() {
    initial_time = std::chrono::steady_clock::now().time_since_epoch().count();
  }

  std::string NormalTime(int time) {
    std::string normaled_time = std::to_string(time);
    if (normaled_time.size() == 1) {
      std::string cur_time = "0";
      for (auto a : normaled_time) {
        cur_time.push_back(a);
      }
      normaled_time = cur_time;
    }
    return normaled_time;
  }

  int GetRestSeconds() {
    cur_time = std::chrono::steady_clock::now().time_since_epoch().count();
    long long delta_time = cur_time - initial_time;
    long long seconds = delta_time / kNanoSecond;
    return seconds;
  }

  void PrintRestTime() {
    int seconds = GetRestSeconds();
    int rest_seconds = kPlaying_time - seconds;
    int rest_minutes = rest_seconds / kSecondsInMinutes;
    rest_seconds %= kSecondsInMinutes;
    std::cout << "The remaining time: " << NormalTime(rest_minutes) << ":" << NormalTime(rest_seconds) << '\n';
  }

  bool LastThirtySeconds() {
    int seconds = GetRestSeconds();
    return (seconds == ThirtySeconds);
  }

  bool LastTenSeconds() {
    int seconds = GetRestSeconds();
    return (seconds == TenSeconds);
  }
};