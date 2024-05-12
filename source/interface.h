#include <fstream>
#include <iostream>
#include <string>

#pragma once

using namespace std;

struct Interface {
    void print_field() {
        ofstream cout("source/connection.json");
        cout << "print_field\n";
    }

    void my_throw(std::vector<int> cubes, std::vector<int> user_change_comb, int number_of_throw) {
        ofstream cout("source/connection.json");
        cout << "my_throw\n";
        for (int i = 1; i <= 5; ++i) {
            cout << cubes[i] << ' ';
        }
        cout << "\n0 ";
        for (int i = 1; i <= 6; ++i) {
            cout << user_change_comb[i] << ' ';
        }
        cout << 0 << ' ';
        for (int i = 8; i <= 14; ++i) {
            cout << user_change_comb[i] << ' ';
        }
        cout << 0 << '\n' << number_of_throw << '\n';
    }

    string return_command() {
        ifstream cin("source/connection.json");
        string command;
        cin >> command;
        return command;
    }

    std::vector<bool> fixed_cubes() {
        ifstream cin("source/connection.json");
        string next;
        cin >> next;
        vector<int> fixed_cubes(5);
        vector<bool> is_fixed(6);
        for (int i = 0; i < 5; ++i) {
            cin >> fixed_cubes[i];
            is_fixed[i + 1] = (bool)fixed_cubes[i];
        }
        return is_fixed;
    }
};