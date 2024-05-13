#include "consts.h"
#include <iostream>
#include <vector>

#pragma once

class Combinations {
public:
  std::vector<int> combination;
  std::vector<int> high_block;
  std::vector<int> low_block;

  void UpdateCombinations(std::vector<int>& comb) {
    high_block.clear();
    low_block.clear();
    high_block.resize(kSix + 1);
    low_block.resize(kSeven + 1);
    combination.resize(kCubesCount + 1);
    for (int i = 1; i <= kCubesCount; ++i) {
      combination[i] = comb[i];
    }
  }

  int GetCubeSum() {
    int sum = 0;
    for (int i = 1; i <= kCubesCount; ++i) {
      sum += combination[i];
    }
    return sum;
  }

  void FillHighBlocks() {
    std::vector<int> count_cube_nums(kSix + 1);
    for (int i = 1; i <= kCubesCount; ++i) {
      ++count_cube_nums[combination[i]];
    }
    for (int i = 1; i <= kSix; ++i) {
      high_block[i] += i * count_cube_nums[i];
    }
  }

  void FillLowBlocks() {
    std::vector<int> count_cube_nums(kSix + 1);
    std::vector<int> flags(kSeven + 1, 0);
    flags[kSeven] = 1;
    for (int i = 1; i <= kCubesCount; ++i) {
      ++count_cube_nums[combination[i]];
      if (count_cube_nums[combination[i]] == 3) {
        flags[1] = 1;
      }
      if (count_cube_nums[combination[i]] == 4) {
        flags[2] = 1;
      }
      if (count_cube_nums[combination[i]] == 5) {
        flags[6] = 1;
        flags[3] = 1;
      }
    }
    for (int i = 1; i <= kSix; ++i) {
      for (int j = 1; j <= kSix; ++j) {
        if ((count_cube_nums[i] == 2 && count_cube_nums[j] == 3) ||
            (count_cube_nums[i] == 3 && count_cube_nums[j] == 2)) {
          flags[3] = 1;
        }
      }
    }
    if ((count_cube_nums[1] >= 1 && count_cube_nums[2] >= 1 && count_cube_nums[3] >= 1 && count_cube_nums[4] >= 1) ||
        (count_cube_nums[2] >= 1 && count_cube_nums[3] >= 1 && count_cube_nums[4] >= 1 && count_cube_nums[5] >= 1) ||
        (count_cube_nums[3] >= 1 && count_cube_nums[4] >= 1 && count_cube_nums[5] >= 1 && count_cube_nums[6] >= 1)) {
      flags[4] = 1;
    }
    if ((count_cube_nums[1] >= 1 && count_cube_nums[2] >= 1 && count_cube_nums[3] >= 1 && count_cube_nums[4] >= 1 && count_cube_nums[5] >= 1) ||
        (count_cube_nums[2] >= 1 && count_cube_nums[3] >= 1 && count_cube_nums[4] >= 1 && count_cube_nums[5] >= 1 && count_cube_nums[6] >= 1)) {
      flags[5] = 1;
    }
    int sum = GetCubeSum();
    std::vector<int> points = {0, sum, sum, 25, 30, 40, 50, sum};
    for (int i = 1; i <= kSeven; ++i) {
      low_block[i] = flags[i] * points[i];
    }
  }

  std::vector<int> GetPotentialPoints() {
    FillHighBlocks();
    FillLowBlocks();
    std::vector<int> points(kSix + kSeven + 1);
    for (int i = 1; i <= kSix + kSeven; ++i) {
      if (i <= kSix) {
        points[i] = high_block[i];
      } else {
        points[i] = low_block[i - kSix];
      }
    }
    return points;
  }

  std::vector<int> PrintPotentialPoints(std::vector<bool>& used) {
    FillHighBlocks();
    FillLowBlocks();
    std::vector<int> cur_points(16, -1);
    int high_sm = 0;
    int low_sm = 0;
    std::cout << '\n';
    for (size_t i = 1; i <= kSix; ++i) {
      if (used[i] == 0) {
        cur_points[i] = high_block[i];
        high_sm += high_block[i];
        std::cout << names[i] << high_block[i] << '\n';
      }
    }
    cur_points[kSeven] = high_sm;
    for (size_t j = 1; j <= kSeven; ++j) {
      if (used[j + kSix] == 0) {
        cur_points[j + kSeven] = low_block[j];
        low_sm += low_block[j];
        std::cout << names[j + kSeven] << low_block[j] << '\n';
      }
    }
    cur_points[15] = low_sm + high_sm;
    return cur_points;
  }
};