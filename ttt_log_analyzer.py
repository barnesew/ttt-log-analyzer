import operator
import re

INPUT_FILE = "ttt_5_9_2020.txt"

ROLES_BY_TEAM = [
    ["innocent", "detective", "mercenary", "glitch", "phantom"],
    ["traitor", "vampire", "assassin", "hypnotist"],
    ["killer"],
    ["zombie"],
    ["jester", "swapper"]
]

DAMAGE_RECORDING_THRESHOLD = 400


def main():

    f = open(INPUT_FILE)
    data = f.read()

    # (player_a, team_a, player_b, team_b, damage)
    damage_instances = re.findall(r"DMG:\s+(.+)\s\[(.+)]\sdamaged\s(.+)\s\[(.+)]\sfor\s(.+)\sdmg", data)
    # (player_a, team_a, player_b, team_b)
    kill_instances = re.findall(r"KILL:\s+(.+)\s\[(.+)]\skilled\s(.+)\s\[(.+)]", data)
    # (player, team)
    env_kill_instances = re.findall(r"KILL:\s+<.+>\skilled\s(.+)\s\[(.+)]", data)

    player_stats = {}

    for damage_instance in damage_instances:

        player_a = damage_instance[0]
        team_a = damage_instance[1]
        player_b = damage_instance[2]
        team_b = damage_instance[3]
        damage = float(damage_instance[4])

        if not (any(team_a in TEAM for TEAM in ROLES_BY_TEAM) and
                any(team_b in TEAM for TEAM in ROLES_BY_TEAM)) or \
                player_a == player_b or \
                float(damage) > DAMAGE_RECORDING_THRESHOLD:
            continue

        init_person(player_a, player_stats)
        init_person(player_b, player_stats)
        was_team_kill = is_teamkill(team_a, team_b)

        if not was_team_kill:
            player_stats[player_a]["damage_given"] += damage
            player_stats[player_b]["damage_taken"] += damage
        else:
            player_stats[player_a]["team_damage_given"] += damage
            player_stats[player_b]["team_damage_taken"] += damage

    for kill_instance in kill_instances:

        player_a = kill_instance[0]
        team_a = kill_instance[1]
        player_b = kill_instance[2]
        team_b = kill_instance[3]

        if not (any(team_a in TEAM for TEAM in ROLES_BY_TEAM) and
                any(team_b in TEAM for TEAM in ROLES_BY_TEAM)) or \
                player_a == player_b:
            continue

        init_person(player_a, player_stats)
        init_person(player_b, player_stats)
        was_team_kill = is_teamkill(team_a, team_b)

        update_increment_tracking_field(player_stats, player_b, "players_killed_by", player_a)
        update_increment_tracking_field(player_stats, player_a, "players_killed", player_b)

        if team_b == "jester":
            player_stats[player_a]["jester_kills"] += 1
            continue
        if not was_team_kill:
            player_stats[player_a]["kills"] += 1
            player_stats[player_b]["deaths"] += 1
        else:
            player_stats[player_a]["team_kills"] += 1
            player_stats[player_b]["deaths_by_team_kill"] += 1

    for env_kill_instance in env_kill_instances:

        player = env_kill_instance[0]
        team = env_kill_instance[1]

        init_person(player, player_stats)

        player_stats[player]["environmental_deaths"] += 1

    print_stats(player_stats)


def init_person(name, player_stats):
    if name in player_stats:
        return
    player_stats[name] = {
        "players_killed_by": {},
        "players_killed": {},
        "kills": 0,
        "team_kills": 0,
        "jester_kills": 0,
        "deaths": 0,
        "deaths_by_team_kill": 0,
        "environmental_deaths": 0,
        "damage_given": 0,
        "team_damage_given": 0,
        "damage_taken": 0,
        "team_damage_taken": 0
    }


def update_increment_tracking_field(player_stats, player_name, field_name, value, number=1):
    if not player_name in player_stats:
        return
    if field_name not in player_stats[player_name]:
        player_stats[player_name][field_name] = {}
    if value not in player_stats[player_name][field_name]:
        player_stats[player_name][field_name][value] = number
    else:
        player_stats[player_name][field_name][value] += number


def is_teamkill(team_a, team_b):
    for TEAM in ROLES_BY_TEAM:
        if team_a in TEAM and team_b in TEAM:
            return True
    return False


def get_keys_with_max_subkey(dictionary, subkey):
    results = ""
    max_value = dictionary[max(dictionary.items(), key=lambda key: key[1][subkey])[0]][subkey]
    for key in dictionary.keys():
        if dictionary[key][subkey] == max_value:
            if len(results) != 0:
                results += ", "
            results += key
    return results, max_value


def get_max_value_keys(dictionary):
    results = ""
    max_value = max(dictionary.items(), key=operator.itemgetter(1))[1]
    for key in dictionary.keys():
        if dictionary[key] == max_value:
            if len(results) != 0:
                results += ", "
            results += key
    return results, max_value


def print_stats(player_stats):

    for player in player_stats.keys():
        if player == "WORLD":
            player_stats[player]["kd"] = 0
            continue
        if player_stats[player]["deaths"] == 0:
            player_stats[player]["kd"] = player_stats[player]["kills"]
        else:
            player_stats[player]["kd"] = player_stats[player]["kills"] / player_stats[player]["deaths"]

    print("\n== GLOBAL STATS ==\n")

    print("Most Kills: %s (%d kills)" % get_keys_with_max_subkey(player_stats, "kills"))
    print("Most Deaths: %s (%d deaths)" % get_keys_with_max_subkey(player_stats, "deaths"))
    print("Highest KD Ratio: %s (%.4f KD ratio)" % get_keys_with_max_subkey(player_stats, "kd"))
    print("Most Damage Given: %s (%.2f damage)" % get_keys_with_max_subkey(player_stats, "damage_given"))
    print("Most Damage Taken: %s (%.2f damage)" % get_keys_with_max_subkey(player_stats, "damage_taken"))
    print("Most Team Kills: %s (%d team kills)" % get_keys_with_max_subkey(player_stats, "team_kills"))
    print("Most Deaths by Team Kill: %s (%d team kill deaths)" %
          get_keys_with_max_subkey(player_stats, "deaths_by_team_kill"))
    print("Most Deaths from the Environment: %s (%d deaths from the environment)" %
          get_keys_with_max_subkey(player_stats, "environmental_deaths"))
    print("Most Jester Kills: %s (%d jester kills)" % get_keys_with_max_subkey(player_stats, "jester_kills"))

    print("\n== PLAYER STATS ==\n")

    for player in player_stats:

        if player_stats[player]["players_killed_by"].keys():
            most_killed_by, most_killed_by_count = get_max_value_keys(player_stats[player]["players_killed_by"])
        else:
            most_killed_by = "Not killed."
            most_killed_by_count = 0
        if player_stats[player]["players_killed"].keys():
            most_killed, most_killed_count = get_max_value_keys(player_stats[player]["players_killed"])
        else:
            most_killed = "No kills."
            most_killed_count = 0

        print(player + ":")
        print("  Kill Count: %d" % player_stats[player]["kills"])
        print("  Death Count: %d" % player_stats[player]["deaths"])
        print("  KD: %.4f" % player_stats[player]["kd"])
        print("  Damage Given: %.1f" % player_stats[player]["damage_given"])
        print("  Damage Taken: %.1f" % player_stats[player]["damage_taken"])
        print("  Team Kills: %d" % player_stats[player]["team_kills"])
        print("  Deaths from Team Kill: %d" % player_stats[player]["deaths_by_team_kill"])
        print("  Deaths from the Environment: %d" % player_stats[player]["environmental_deaths"])
        print("  Team Damage Given: %.1f" % player_stats[player]["team_damage_given"])
        print("  Team Damage Taken: %.1f" % player_stats[player]["team_damage_taken"])
        print("  Jester Kills: %d" % player_stats[player]["jester_kills"])
        print("  Most Killed By: %s (%d times)" % (most_killed_by, most_killed_by_count))
        print("  Player Most Killed: %s (%d times)" % (most_killed, most_killed_count))
        print()


if __name__ == "__main__":
    main()
