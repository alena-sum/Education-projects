import Main
import argparse

import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choosing a type of generate\n")
    parser.add_argument("-t", "--type", default=0, help="type of generate,\n 0 -> Create in game"
                                                        "\n 1 -> DFS,\n 2 -> MST")
    args = parser.parse_args()
    g1 = Main.Game(args, [config.UP, config.DOWN, config.RIGHT, config.LEFT])
    g1.prev_game()
