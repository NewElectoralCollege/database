import csv
import math
import json

# Remember that the essay Programmer's Guide to Proportional Representation needs to be updated with the correct lines if this file is edited.

allocations = {
    'Alabama': [9, 9, 9, 9, 9],
    'Alaska': [3, 3, 3, 3, 3],
    'Arizona': [6, 7, 8, 10, 11],
    'Arkansas': [6, 6, 6, 6, 6],
    'California': [45, 47, 54, 55, 55],
    'Colorado': [7, 8, 8, 9, 9],
    'Connecticut': [8, 8, 8, 7, 7],
    'Delaware': [3, 3, 3, 3, 3],
    'District of Columbia': [3, 3, 3, 3, 3],
    'Florida': [17, 21, 25, 27, 29],
    'Georgia': [12, 12, 13, 15, 16],
    'Hawaii': [4, 4, 4, 4, 4],
    'Idaho': [4, 4, 4, 4, 4],
    'Illinois': [26, 24, 22, 21, 20],
    'Indiana': [13, 12, 12, 11, 11],
    'Iowa': [8, 8, 7, 7, 6],
    'Kansas': [7, 7, 6, 6, 6],
    'Kentucky': [9, 9, 8, 8, 8],
    'Louisiana': [10, 10, 9, 9, 8],
    'Maine': [4, 4, 4, 4, 4],
    'Maryland': [10, 10, 10, 10, 10],
    'Massachusetts': [14, 13, 12, 12, 11],
    'Michigan': [21, 20, 18, 17, 16],
    'Minnesota': [10, 10, 10, 10, 10],
    'Mississippi': [7, 7, 7, 6, 6],
    'Missouri': [12, 11, 11, 11, 10],
    'Montana': [4, 4, 3, 3, 3],
    'Nebraska': [5, 5, 5, 5, 5],
    'Nevada': [3, 4, 4, 5, 6],
    'New Hampshire': [4, 4, 4, 4, 4],
    'New Jersey': [17, 16, 15, 15, 14],
    'New Mexico': [4, 5, 5, 5, 5],
    'New York': [41, 36, 33, 31, 29],
    'North Carolina': [13, 13, 14, 15, 15],
    'North Dakota': [3, 3, 3, 3, 3],
    'Ohio': [25, 23, 21, 20, 18],
    'Oklahoma': [8, 8, 8, 7, 7],
    'Oregon': [6, 7, 7, 7, 7],
    'Pennsylvania': [27, 25, 23, 21, 20],
    'Rhode Island': [4, 4, 4, 4, 4],
    'South Carolina': [8, 8, 8, 8, 9],
    'South Dakota': [4, 3, 3, 3, 3],
    'Tennessee': [10, 11, 11, 11, 11],
    'Texas': [26, 29, 32, 34, 38],
    'Utah': [4, 5, 5, 5, 6],
    'Vermont': [3, 3, 3, 3, 3],
    'Virginia': [12, 12, 13, 13, 13],
    'Washington': [9, 10, 11, 11, 12],
    'West Virginia': [6, 6, 5, 5, 5],
    'Wisconsin': [11, 11, 11, 10, 10],
    'Wyoming': [3, 3, 3, 3, 3],

}


def getElectors(state, year):
    try:
        census = math.floor((int(year) - 1) / 10) - 197
    except ValueError:
        print(year)

    try:
        return allocations[state][census]
    except KeyError:
        return 10


class List:
    def __init__(self, name, votes, candidate):
        self.name = name
        self.votes = int(votes)
        self.candidate = candidate
        self.real = not(candidate == "Invalid")


class Nominee:
    def __init__(self, name, party, votes):
        self.name = name
        self.party = party
        self.votes = votes
        self.extra_votes = votes
        self.extra_seat = False
        self.seats = 0


class Election:
    def __init__(self, state, year):
        self.lists: 'list[List]' = []
        self.state = state
        self.year = year
        self.total_seats = getElectors(state, year)
        self.candidates: 'list[Nominee]' = []

    def parties(self):
        pts = []

        for candidate in self.candidates:
            pts.append(
                {"name": candidate.party,
                 "seats": candidate.seats,
                 "votes": candidate.votes,
                 "extra_votes": candidate.extra_votes,
                 "extra_seat": candidate.extra_seat
                 }
            )

        return pts

    def stats(self):
        results = {
            "name": self.state + " " + self.year,
            "total_seats": self.total_seats,
            "total_votes": self.total_votes(),
            "gallagher_index": self.gallagher_index()
        }

        return results

    def total_votes(self):
        total = 0

        for list in self.lists:
            if list.real:
                total += int(list.votes)

        return total

    def gallagher_index(self):
        cs = 0

        for candidate in self.candidates:
            cs += pow((candidate.votes / self.total_votes() * 100) -
                      (candidate.seats / self.total_seats * 100), 2)

        return pow(0.5 * cs, 0.5)

    # makeResults.py

    def run(self):
        nds = {}

        for list in self.lists:
            if list.real:
                try:
                    nds[list.candidate] += list.votes
                except KeyError:
                    nds[list.candidate] = list.votes

        for candidate in nds:
            self.candidates.append(
                Nominee(candidate, self.partyOfCandidate(candidate), nds[candidate]))

        quota = math.floor(self.total_votes() / self.total_seats)
        assigned = 0

        for candidate in self.candidates:
            candidate.seats = math.floor(candidate.votes / quota)
            candidate.extra_votes = candidate.votes - (candidate.seats * quota)

            assigned += candidate.seats

        def extra_votes(elem):
            return elem.extra_votes

        self.candidates.sort(key=extra_votes, reverse=True)

        while assigned < self.total_seats:
            c = self.candidates[0]

            c.extra_seat = True
            c.seats += 1

            self.candidates.append(c)
            del self.candidates[0]

            assigned += 1

    def partyOfCandidate(self, candidate: str):
        party = (-1, "")

        for list in self.lists:
            if list.votes > party[0] and list.candidate == candidate:
                party = (list.votes, list.name)

        if party[1] == "Independent":
            party = (party[0], "Independent - " + candidate)

        return party[1]


elections = {}

with open("./data/database.csv", "r") as file:
    lines = csv.reader(file)

    for year, state, candidate, party, votes in lines:
        if "Header" in year:
            continue

        try:
            elections[state + "-" +
                      year].lists.append(List(party, votes, candidate))
        except KeyError:
            election = Election(state, year)
            election.lists.append(List(party, votes, candidate))
            elections[state + "-" + year] = election

for election in elections.values():
    file = open("./data/" + election.year + "/" +
                election.state + ".json", "w")

    election.run()

    data = {
        "parties": election.parties(),
        "stats": election.stats()
    }

    file.write(json.dumps(data))

    file.close()
