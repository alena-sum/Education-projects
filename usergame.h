#include <iostream>
#include <vector>
#include "board.h"
#include "combinations.h"
#include "cubes.h"
#include "consts.h"

#pragma once

class UserGame : Cubes, Combinations, public Board {
    std::vector<int> used_combs;
public:
    UserGame() {
        used_combs.resize(kSix + kSeven + 1, 0);
        UpdateCubes();
        UpdateCombinations(numbers);
        UpdateBoard();
    }
    void PrintChooseText() {
        std::cout << "Choose number of suitable combination\n(1 -"
                     " ones\n2 - twos\n3 - threes\n4 - fours\n5 - "
                     "fives\n6 - sixes\n7 - 3x\n8 - 4x\n9 - 3x + 2y\n10 - "
                     "small street\n11 - large street\n12 - general\n13 "
                     "- chance)\nor print 'next' to repeat the throw:";
    }
    void UserTurn(int number_of_throw) {
        UpdateCombinations(numbers);
        if (number_of_throw == 1) {
            std::cout << "\nNow it's your turn!\nYour cubes: ";
            PrintCubes();
        }
        PrintPotentialPoints(used_combs);
        if (number_of_throw == 3) {
            std::cout << "Please, choose number of suitable combination\n(1 -"
                         " ones\n2 - twos\n3 - threes\n4 - fours\n5 - "
                         "fives\n6 - sixes\n7 - 3x\n8 - 4x\n9 - 3x + 2y\n10 - "
                         "small street\n11 - large street\n12 - general\n13 "
                         "- chance)\n";
        } else {
            PrintChooseText();
        }
        std::string command;
        std::cin >> command;
        if (command == "next" && number_of_throw != 3) {
            ChooseCubes();
            ThrowCubes();
            std::cout << "Your cubes: ";
            PrintCubes();
        } else if (std::stoi(command) >= 1 && std::stoi(command) <= kSix + kSeven && used_combs[std::stoi(command)] != 1) {
            int icommand = std::stoi(command);
            used_combs[icommand] = 1;
            int points;
            if (icommand <= 6) {
                points = high_block[icommand];
            } else {
                points = low_block[icommand - kSix];
            }
            Update(std::stoi(command), points);
            std::cout << "\nYour score:\n";
            PrintBoard();
            ThrowCubes();
            return;
        } else {
            std::cout << "Incorrect input. Try again, please.\n";
            UserTurn(number_of_throw);
        }
        ++number_of_throw;
        UserTurn(number_of_throw);
    }
};