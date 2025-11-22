def format_output(overall, details, word_count):
    return {
        "overall_score": overall,
        "word_count": word_count,
        "criteria_results": details
    }
