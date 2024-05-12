#include <algorithm>
#include <iostream>
#include <map>
#include <vector>
#pragma once

bool cmp(std::pair<int, double> first_elem, std::pair<int, double> second_elem) {
    bool fl1 = first_elem.second > second_elem.second;
    bool fl2 = first_elem.second == second_elem.second;
    bool fl3 = first_elem.first >= 1 && first_elem.first <= 4 && second_elem.first >= 7 && second_elem.first <= 8;
    bool fl4 = second_elem.first >= 1 && second_elem.first <= 4 && first_elem.first >= 7 && first_elem.first <= 8;
    bool fl5 = first_elem.first > second_elem.first;
    return fl1 || (fl2 && fl3) || (fl3 && fl5 && !fl4);
}

class FindProbabilities {
   public:
    std::vector<std::vector<int>> fix_cubes;
    std::vector<std::pair<int, double>> probabilities;
    std::vector<int> count;
    std::vector<std::vector<int>> val_indexes;
    const double kPr = 1.0 / kDSix;

    double Cnk(int n, int k) {
        double answer = 1.0;
        for (int i = n; i > k; --i) {
            answer *= i;
        }
        for (int i = 1; i <= n - k; ++i) {
            answer /= (double) i;
        }
        return answer;
    }

    void UpdateProbab345(int ind, int mult, int cnt_i, double& mx_prob) {
        int comb = kSeven;
        double prob = pow(kPr, std::max(mult - cnt_i, 0)) * Cnk(kCubesCount - cnt_i, std::max(mult - cnt_i, 0));
        if (mx_prob <= prob) {
            if (mult == 4) comb++;
            if (mult == 5) comb = kSeven + 5;
            fix_cubes[comb] = val_indexes[ind];
            mx_prob = prob;
        }
        return;
    }

    void Add16(int ind, int cnt_i) {
        double prob = pow(kPr, std::max(3 - cnt_i, 0)) * Cnk(kCubesCount - cnt_i, std::max(3 - cnt_i, 0));
        probabilities.push_back({ind, prob});
        fix_cubes[ind] = val_indexes[ind];
        return;
    }

    void SmallStraight() {
        std::map<std::vector<int>,double> mp;
        for (int start = 1; start <= 3; ++start) {
            std::vector<int>cur_fix;
            for (int i = start; i < start + 4; ++i) {
                if (count[i] != 0) {
                    cur_fix.push_back(val_indexes[i][0]);
                }
            }
            int sz = cur_fix.size();
            double prob = std::pow(kPr, 4 - sz);
            for (int i = 0; i < 4 - sz; ++i) {
                prob *= (5 - i - sz);
            }
            mp[cur_fix] += prob;
        }
        double probab_small_str = 0.0;
        std::vector<int> fixed_cub;
        for (auto a : mp) {
            if (a.second > probab_small_str) {
                probab_small_str = a.second;
                fixed_cub = a.first;
            }
        }
        probabilities.push_back({kSeven + 3, probab_small_str});
        fix_cubes[kSeven + 3] = fixed_cub;
    }


    void LargeStraight() {
        std::map<std::vector<int>,double> mp;
        for (int start = 1; start <= 2; ++start) {
            std::vector<int>cur_fix;
            for (int i = start; i < start + 5; ++i) {
                if (count[i] != 0) {
                    cur_fix.push_back(val_indexes[i][0]);
                }
            }
            int sz = cur_fix.size();
            double prob = std::pow(kPr, 5 - sz);
            for (int i = 0; i < 5 - sz; ++i) {
                prob *= (5 - i - sz);
            }
            mp[cur_fix] += prob;
        }
        double probab_large_str = 0.0;
        std::vector<int> fixed_cub;
        for (auto a : mp) {
            if (a.second > probab_large_str) {
                probab_large_str = a.second;
                fixed_cub = a.first;
            }
        }
        probabilities.push_back({kSeven + 4, probab_large_str});
        fix_cubes[kSeven + 4] = fixed_cub;
    }

    double Pr23(int i, int j) {
        double cur_prob = pow(kPr, std::max(2 - count[i], 0)) * pow(kPr, std::max(3 - count[j], 0));
        cur_prob *= Cnk(kCubesCount - count[j] - count[i], std::max(2 - count[i], 0));
        cur_prob *= Cnk(kCubesCount - count[j] - 2, std::max(3 - count[j], 0));
        return cur_prob;
    }

    void Comb32x() {
        double probab23 = 0.0;
        for (int i = 1; i <= kSix; ++i) {
            for (int j = 1; j <= i; ++j) {
                double cur_prob = Pr23(i, j) + Pr23(j, i);
                if (i == j) {
                    cur_prob = std::pow(kPr, 5 - count[i]);
                }
                if (probab23 < cur_prob) {
                    probab23 = cur_prob;
                    std::vector<int> i_indexes;
                    for (int cur = 0; cur < std::min(2, count[i]); ++cur) i_indexes.push_back(val_indexes[i][cur]);
                    int cur0 = 0;
                    if (i == j) cur0 = std::min(2, count[i]);
                    for (int cur = cur0; cur < std::min(cur0 + 3, count[j]); ++cur) i_indexes.push_back(val_indexes[j][cur]);
                    fix_cubes[kSeven + 2] = i_indexes;
                }
            }
        }
        probabilities.push_back({kSeven + 2, probab23});
    }

    void UpdateProbability(std::vector<int>& current_numbers) {
        probabilities.clear();
        fix_cubes.clear();
        val_indexes.clear();
        count.clear();
        fix_cubes.resize(kSix + kSeven);
        count.resize(kSix + 1);
        val_indexes.resize(kSix + 1);
        double mx_low_prob3 = 0.0;
        double mx_low_prob4 = 0.0;
        double mx_low_prob5 = 0.0;
        for (int i = 1; i <= kSix; ++i) {
            int cnt_i = 0;
            for (size_t j = 1; j <= kCubesCount; ++j) {
                if (current_numbers[j] == i) {
                    cnt_i++;
                    val_indexes[i].push_back(j);
                }
            }
            count[i] = cnt_i;
            UpdateProbab345(i, 3, cnt_i, mx_low_prob3);
            Add16(i, cnt_i);// (1-6)
            UpdateProbab345(i, 4, cnt_i, mx_low_prob4);
            UpdateProbab345(i, 5, cnt_i, mx_low_prob5);
        }
        probabilities.push_back({kSeven, mx_low_prob3});    // 3x
        probabilities.push_back({kSeven + 1, mx_low_prob4});// 4x
        Comb32x(); // 3x+2y
        SmallStraight(); // Small Straight
        LargeStraight(); // Large Straight
        probabilities.push_back({kSeven + 5, mx_low_prob5}); // general
        std::sort(probabilities.begin(), probabilities.end(), cmp);
        std::vector<int> prior;
        for (auto a : probabilities) {
            prior.push_back(a.first);
        }
    }

    std::vector<std::pair<int, double>> ReturnProb() {
        return probabilities;
    }

    std::vector<std::vector<int>> ReturnFixInd() {
        return fix_cubes;
    }
};