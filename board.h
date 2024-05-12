#include "consts.h"
#include <iostream>
#include <vector>

#pragma once

class Board {
  std::vector<int> current_score;
  int high_block_points = 0;
  bool flag = false;

 public:
  int all_points = 0;

  void UpdateBoard() {
    current_score.resize(kSix + kSeven + 1);
  }

  void Update(int command, int points) {
    current_score[command] = points;
    all_points += points;
    if (command <= 6) {
      high_block_points += points;
    }
    if (high_block_points >= kBorder && flag == false) {
      high_block_points += kDop;
      all_points += kDop;
      flag = true;
    }
  }

  void PrintBoard() {
    for (size_t i = 1; i <= kSix; ++i) {
      std::cout << names[i] << current_score[i] << '\n';
    }
    std::cout << names[kSeven] << high_block_points << '\n';
    for (size_t i = 1; i <= kSeven; ++i) {
      std::cout << names[i + kSeven] << current_score[i + kSix] << '\n';
    }
    std::cout << names[kSeven + kSeven + 1] << all_points << '\n';
  }

  int ReturnFinalScore() {
    return all_points;
  }

};