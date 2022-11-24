class League(object):
    def __init__(self):
        self.persons = dict()

    def print_basic_txt_statistics(self):
        for person in self.persons.values():
            print(f"{person.name} {person.get_basic_txt_statistics()}")


class Person(object):
    def __init__(self, name):
        self.name = name
        self.matches = []

    def get_basic_txt_statistics(self):
        positions = {i: 0 for i in range(-1, 4)}
        for match in self.matches:
            positions[match.get_position(self.name)] += 1

        return f"Wins: {positions[0]+positions[1]} ({positions[0]} as defender, {positions[1]} as attacker), Losses: {positions[2]+positions[3]} ({positions[2]} as defender, {positions[3]} as attacker), W/L Ratio: {round((positions[0]+positions[1])/(positions[2]+positions[3]), 2) if (positions[2]+positions[3]) != 0 else (positions[0]+positions[1])}"


class Match(object):
    def __init__(self, winning_defender, winning_attacker, losing_defender, losing_attacker, round=None, crawling=False):
        self.winning_defender = winning_defender
        self.winning_attacker = winning_attacker
        self.losing_defender = losing_defender
        self.losing_attacker = losing_attacker

        self.round = round
        self.crawling = crawling

    def get_position(self, name):
        if name == self.winning_defender:
            return 0
        elif name == self.winning_attacker:
            return 1
        elif name == self.losing_defender:
            return 2
        elif name == self.losing_attacker:
            return 3
        else:
            return -1


def process_matches(matches):
    league = League()

    all_persons = []
    for match in matches:
        _, winning_defender, winning_attacker, losing_defender, losing_attacker, _ = match.split(';')
        all_persons.append(winning_defender)
        all_persons.append(winning_attacker)
        all_persons.append(losing_defender)
        all_persons.append(losing_attacker)
    all_persons = set(all_persons)

    for person in all_persons:
        league.persons[person] = Person(person)

    for match in matches:
        round, winning_defender, winning_attacker, losing_defender, losing_attacker, crawling = match.split(';')
        match = Match(winning_defender, winning_attacker, losing_defender, losing_attacker, int(round), bool(crawling))
        for player in [winning_defender, winning_attacker, losing_defender, losing_attacker]:
            league.persons[player].matches.append(match)

    return league


if __name__ == '__main__':
    with open('scores.txt') as file:
        matches = [line.rstrip() for line in file]

    league = process_matches(matches)
    league.print_basic_txt_statistics()
