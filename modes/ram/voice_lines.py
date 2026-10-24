"""Original spoken lines and stable event names shared by generation and wiring."""

NUMBER_WORDS = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "twenty one", "twenty two",
    "twenty three", "twenty four", "twenty five",
)


def center_lines():
    lines = {
        f"ram_center_kills_{amount:02d}_v2": {
            "kind": "center_kills", "amount": amount,
            "text": f"You earned {NUMBER_WORDS[amount]} bonus "
                    f"{'kill' if amount == 1 else 'kills'} at the center!",
        }
        for amount in range(1, 26)
    }
    # Keep the shortest, most easily blended numbers distinct in speech.
    for amount in (2, 8):
        lines[f"ram_center_kills_{amount:02d}_v2"]["text"] = (
            f"{NUMBER_WORDS[amount].capitalize()} extra kills for center control!"
        )
    lines["ram_center_reinforcements_v2"] = {
        "kind": "center_reinforcements", "text": "Center reinforcements have arrived!",
    }
    for state, name, text in (
        (1, "team1", "Team number one controls the center!"),
        (2, "team2", "Team number two controls the center!"),
        (3, "contested", "The center is contested!"),
        (4, "neutral", "The center is neutral."),
    ):
        lines[f"ram_center_{name}_v2"] = {"kind": "center_status", "state": state, "text": text}
    return lines


def signal_lines():
    """Stable event ids also encode which team may receive a command."""
    lines = {}
    for color in range(1, 9):
        word = NUMBER_WORDS[color]
        for kind, offset, text in (
            ("help", 0, f"Player number {word} needs help!"),
            ("attack", 8, f"Let's attack player number {word}!"),
            ("feed", 16, f"Player number {word}. Stop giving away kills!"),
        ):
            lines[f"ram_team_{kind}_p{color}_v2"] = {
                "kind": "team_signal", "signal": kind, "target": color,
                "event": offset + color, "text": text,
            }
    return lines
