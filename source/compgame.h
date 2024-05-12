#include <iostream>
#include <vector>
#include "probability.h"
#include "board.h"
#include "combinations.h"
#include "cubes.h"
#include "consts.h"

#pragma once

std::vector<int> priority_for_zero = {0, 1, 12, 8, 11, 9, 2, 3, 4, 5, 6, 10, 7};

class CompGame : FindProbabilities, public Board, Combinations, Cubes {
  std::vector<int> used_combs;
 public:
  CompGame() {
    used_combs.resize(kSix + kSeven + 1, 0);
    UpdateCubes();
    UpdateProbability(numbers);
    UpdateCombinations(numbers);
    UpdateBoard();
  }
  void MachineTurn(int number_of_throw) {
    UpdateCombinations(numbers);
    UpdateProbability(numbers);
    if (number_of_throw == 1) {
      std::cout << "\nNow it's computer turn.\nIts cubes: ";
      PrintCubes();
    }
    std::vector<int> points = GetPotentialPoints();
    int point = 0;
    int ind_point = 0;
    for (int i = 0; i < kSix + kSeven; ++i) {
      if (probabilities[i].second == 1 && !(probabilities[i].first == 7 ||
                                            probabilities[i].first == 10) && used_combs[probabilities[i].first] == 0) {
        used_combs[probabilities[i].first] = 1;
        Update(probabilities[i].first, points[probabilities[i].first]);
        std::cout << "\nComp's score:\n";
        PrintBoard();
        ThrowCubes();
        return;
      } else if (used_combs[probabilities[i].first] == 0) {
        ind_point = probabilities[i].first;
        point = points[ind_point];
        break;
      }
    }
    if ((point == 0 || (ind_point >= 1 && ind_point <= 6 && point / ind_point <= 2)) && number_of_throw == 3) {
      if (used_combs[kSix + kSeven] == 0) {
        point = points[kSix + kSeven];
        ind_point = kSix + kSeven;
      }
    }
    if (point == 0 && number_of_throw == 3) {
      for (int i = 1; i < kSix + kSeven; ++i) {
        if (used_combs[priority_for_zero[i]] == 0) {
          ind_point = priority_for_zero[i];
          break;
        }
      }
    }
    if (number_of_throw == 3) {
      used_combs[ind_point] = 1;
      Update(ind_point, point);
      std::cout << "\nComp's score:\n";
      PrintBoard();
      ThrowCubes();
      return;
    }
    FixCubes(fix_cubes[ind_point]);
    ThrowCubes();
    std::cout << "\nIts cubes: ";
    PrintCubes();
    ++number_of_throw;
    MachineTurn(number_of_throw);
  }
};