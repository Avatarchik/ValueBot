import configparser


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "login_pos", "ochko")
    config.set("Settings", "pass_pos", "hrena.ua")
    config.set("Settings", "login_bet", "JuliaDauris")
    config.set("Settings", "pass_bet", "Nbuh73799899")
    config.set("Settings", "bet_mirror", "838365.com/en/")
    config.set("Settings", "fix_bet", "10")
    config.set("Settings", "max_one_game_count", "8")

    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "config.txt"
    createConfig(path)