#include "board.h"
#include "combinations.h"
#include "cubes.h"
#include "probability.h"
#include "compgame.h"
#include "usergame.h"
#include <algorithm>
#include <iostream>

void PrintResults(UserGame& player, CompGame& machine) {
  std::cout << "\nTHE END!\n";
  std::string winner;
  if (player.ReturnFinalScore() == machine.ReturnFinalScore()) {
    std::cout << "DRAW";
    return;
  }
  winner = player.ReturnFinalScore() > machine.ReturnFinalScore() ? "YOU" : "STUPID ROBOT";
  std::cout << winner << " WON";
}

int main() {
  CompGame comp;
  UserGame user;
  for (size_t i = 1; i <= kSix + kSeven; ++i) {
    user.UserTurn(1);
    comp.MachineTurn(1);
  }
  PrintResults(user, comp);
}