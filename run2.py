import Main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choosing a type of generate\n")
    parser.add_argument("-t", "--type", default=0, help="type of generate,\n 0 -> Create in game"
                                                        "\n 1 -> DFS,\n 2 -> MST")
    args = parser.parse_args()
    g2 = Main.Game(args, ["W", "S", "D", "A"])
    g2.prev_game()