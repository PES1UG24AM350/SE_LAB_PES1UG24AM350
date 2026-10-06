import json
import os


SCORE_FILE = "high_scores.json"
MAX_SCORES = 5


def load_scores():
    """
    Load high scores from JSON file.
    """

    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, "r") as file:
            scores = json.load(file)

        if not isinstance(scores, list):
            return []

        return scores

    except (json.JSONDecodeError, OSError):
        return []


def save_score(score):
    """
    Add a score to the high-score table.

    Only the top 5 scores are retained.
    """

    scores = load_scores()

    scores.append(score)

    # Highest score first
    scores.sort(reverse=True)

    # Keep only top 5
    scores = scores[:MAX_SCORES]

    try:
        with open(SCORE_FILE, "w") as file:
            json.dump(scores, file, indent=4)
    except OSError:
        pass

    return scores


def get_high_scores():
    """
    Return the current top 5 scores.
    """

    return load_scores()
