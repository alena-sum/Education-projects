#include "source/board.h"
#include "source/combinations.h"
#include "source/cubes.h"
#include "source/compgame.h"
#include "source/interface.h"
#include "source/probability.h"
#include "source/usergame.h"
#include <algorithm>
#include <cstdlib>
#include <fstream>
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
  Interface interface;
  interface.print_field();
  for (size_t i = 1; i <= kSix + kSeven; ++i) {
    user.UserTurn(1);
    comp.MachineTurn(1);
  }
  PrintResults(user, comp);
}
