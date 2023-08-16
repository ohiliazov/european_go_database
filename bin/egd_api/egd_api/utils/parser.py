import pandas as pd
from pydantic import BaseModel


class RoundResult(BaseModel):
    opponent_place: int
    result: str
    handicap: int


class PlayerResults(BaseModel):
    place: int
    last_name: str
    first_name: str
    rank: str
    country: str
    club: str
    points: list[float]
    egd_pin: str | None = None


def parse_tournament_info(path: str) -> list[str]:
    header = []
    with open(path) as file:
        for line in file.readlines():
            if line.startswith(";"):
                header.append(line)
            else:
                break
    return header


def parse_player_results(row):
    place, full_name, rank, country, club, *rest = row
    points, rounds, egd_pin = [], [], None

    for value in rest:
        if isinstance(value, (int, float)):
            points.append(value)
        elif value.startswith("|"):
            egd_pin = value[1:]
        else:
            rounds.append(value)

    last_name, first_name = full_name.split()

    return (
        PlayerResults(
            place=place,
            last_name=last_name,
            first_name=first_name,
            rank=rank,
            country=country,
            club=club,
            points=points,
            rounds=rounds,
            egd_pin=egd_pin,
        ),
        rest,
    )


def parse_tournament_results(filename: str, skip_rows: int):
    data = []
    for idx, item in pd.read_fwf(filename, skiprows=skip_rows).iterrows():
        data.append(parse_player_results(item))
    return data


def parse_tournament(filename: str):
    tournament_info = parse_tournament_info(filename)

    results = parse_tournament_results(filename, len(tournament_info))

    return tournament_info, results


if __name__ == "__main__":
    filepath = "/home/oleksandr.hiliazov/PycharmProjects/european_go_database/bin/egd_api/egd_api/utils/data.txt"

    tinfo, tresults = parse_tournament(filepath)

    print(tinfo)
    print(tresults)
