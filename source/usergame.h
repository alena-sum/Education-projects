#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include "board.h"
#include "combinations.h"
#include "cubes.h"
#include "consts.h"
#include <fstream>
#include "interface.h"

#pragma once

bool use_term = 0;

using namespace std::this_thread;
using namespace std::chrono; 

class UserGame : Cubes, Combinations, public Board {
    std::vector<bool> used_combs;
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
        Interface interface;
        UpdateCombinations(numbers);
        if (number_of_throw == 1) {
            std::cout << "\nNow it's your turn!\nYour cubes: ";
            PrintCubes();
            std::vector<int> user_change_comb = PrintPotentialPoints(used_combs);
            interface.my_throw(ReturnCubes(), user_change_comb, number_of_throw);
        }
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
        command = interface.return_command();
        if (use_term) std::cin >> command;
        while (command == "" || command == "my_throw" || command == "print_field") {
            command = interface.return_command();
        }
        if (command == "next" && number_of_throw != 3) {
            if (use_term) {
                ChooseCubes();
            } else {
                sleep_for(nanoseconds(2000000000));
                fixed_cubes = interface.fixed_cubes();
            }
            ThrowCubes();
            UpdateCombinations(numbers);
            std::cout << "Your cubes: ";
            PrintCubes();
            std::vector<int> user_change_comb = PrintPotentialPoints(used_combs);
            interface.my_throw(ReturnCubes(), user_change_comb, number_of_throw);


        } else if (std::stoi(command) >= 1 && std::stoi(command) <= kSix + kSeven && used_combs[std::stoi(command)] != 1) {
            int icommand = std::stoi(command);
            used_combs[icommand] = 1;
            int points;
            FillHighBlocks();
            FillLowBlocks();
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