#include "consts.h"
#include <iostream>
#include <random>
#include <vector>
#include <chrono>

#pragma once

std::mt19937 rnd(std::chrono::steady_clock::now().time_since_epoch().count());

class Cubes {
 public:
  std::vector<int> numbers;
  std::vector<bool> fixed_cubes;

  void UpdateCubes() {
    numbers.resize(kCubesCount + 1);
    fixed_cubes.resize(kCubesCount + 1);
    for (size_t i = 1; i <= kCubesCount; ++i) {
      numbers[i] = rnd() % kSix + 1;
    }
  }

  int GenerateValue() {
    int value = rnd() % kSix + 1;
    return value;
  }

  void FixCubes(std::vector<int>& to_fix) {
    for (int number : to_fix) {
      fixed_cubes[number] = 1;
    }
  }

  void ChooseCubes() {
    std::cout << "\nPlease, print the cubes you want to fix: ";
    std::string fixed_cubes_str;
    std::getline(std::cin, fixed_cubes_str);
    std::getline(std::cin, fixed_cubes_str);

    std::cout << '\n';
    for (auto number_str : fixed_cubes_str) {
      int number = number_str - '0';
      if (number >= 1 && number <= kCubesCount) {
        fixed_cubes[number] = 1;
      }
    }
  }

  void ThrowCubes() {
    for (size_t i = 1; i <= kCubesCount; ++i) {
      if (fixed_cubes[i] == 0) {
        numbers[i] = GenerateValue();
      }
    }
    fixed_cubes.assign(kCubesCount + 1, 0);
  }

  void PrintCubes() {
    for (size_t i = 1; i <= kCubesCount; ++i) {
      std::cout << numbers[i] << ' ';
    }
  }

  std::vector<int> ReturnCubes() {
    return numbers;
  }
};