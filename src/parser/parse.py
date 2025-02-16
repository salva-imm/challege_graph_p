import csv
import re
from collections import defaultdict


def extract_mentions(text: str) -> list[str]:
    # NOTE: this logic might be faulty! b/c I didn't count the number of mentions : )
    pattern = r"@\w+"
    return re.findall(pattern, text)

def extractor():
    filename = "parser/samples.csv"
    mentions_list = []
    mention_counts = defaultdict(int)
    with open(filename, mode="r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            tweet_text = row['data'].strip('"') if row['data'].startswith(
                '"') else row['data'].strip('"""')
            user = row.get("username", "unknown")

            mentions = extract_mentions(tweet_text)
            for m in mentions:
                mention_counts[(user, m)] += 1
        mentions_list = [
            {"source_username": source, "target_username": target,
             "weight": weight}
            for (source, target), weight in mention_counts.items()
        ]
        return mentions_list

if __name__ == "__main__":
    print(extractor())