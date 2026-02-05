def run_base_engine(content_id, data):
    perf = data["performance"][content_id]
    rel = data["relative"][content_id]
    hist = data["history"][content_id]
    qual = data["qualitative"][content_id]
    intent = data["intent"][content_id]
    temporal = data["temporal"][content_id]

    impressions = perf["impressions"]

    total_engagement = (
        perf["likes"] +
        perf["comments"] +
        perf["shares"] +
        perf["saves"]
    )

    engagement_rate = total_engagement / impressions
    save_rate = perf["saves"] / impressions
    share_rate = perf["shares"] / impressions

    dominant_engagement = max(
        ["likes", "comments", "shares", "saves"],
        key=lambda x: perf[x]
    )

    # --- Performance Status ---
    if rel["performance_vs_avg"] < 0.8:
        performance_status = "underperforming"
    elif rel["performance_vs_avg"] <= 1.2:
        performance_status = "average"
    else:
        performance_status = "outperforming"

    # --- Content Value ---
    if save_rate > 0.02:
        content_value = "educational"
    elif share_rate > 0.015:
        content_value = "viral"
    elif dominant_engagement == "comments":
        content_value = "discussion"
    elif dominant_engagement == "likes":
        content_value = "inspirational"
    else:
        content_value = "weak"

    # --- Hook Strength ---
    if perf["dropoff_rate"] and perf["dropoff_rate"] > 0.4:
        hook_strength = "weak"
    elif rel["engagement_velocity"] == "fast":
        hook_strength = "strong"
    else:
        hook_strength = "medium"

    # --- Topic Fatigue ---
    if hist["topic_fatigue_score"] > 0.5:
        fatigue_level = "high"
    elif hist["topic_fatigue_score"] > 0.3:
        fatigue_level = "medium"
    else:
        fatigue_level = "low"

    overposting = hist["similar_past_posts"] > 6

    # --- Audience Alignment ---
    if qual["comment_sentiment"] in ["negative", "mixed"] and intent["emotional_intent"] == "inspire":
        intent_match = "misaligned"
    else:
        intent_match = "aligned"

    # --- Timing Quality ---
    posted_time = temporal["posting_datetime"].split("T")[1][:5]  # HH:MM
    posted_hour = int(posted_time.split(":")[0])

    best_time_match = False

    for slot in hist["best_time_slots"]:
      start, end = slot.split("-")
      start_hour = int(start.split(":")[0])
      end_hour = int(end.split(":")[0])

    if start_hour <= posted_hour < end_hour:
        best_time_match = True

    timing_quality = "good" if best_time_match else "average"

    return {
        "content_id": content_id,
        "performance_status": performance_status,
        "engagement_profile": {
            "engagement_rate": round(engagement_rate, 4),
            "save_rate": round(save_rate, 4),
            "share_rate": round(share_rate, 4),
            "dominant_engagement": dominant_engagement
        },
        "content_value_type": content_value,
        "hook_analysis": {
            "hook_strength": hook_strength,
            "dropoff_flag": perf["dropoff_rate"] and perf["dropoff_rate"] > 0.4
        },
        "topic_health": {
            "fatigue_level": fatigue_level,
            "overposting_flag": overposting
        },
        "audience_alignment": {
            "intent_match": intent_match,
            "comment_sentiment": qual["comment_sentiment"]
        },
        "distribution_health": {
            "timing_quality": timing_quality,
            "decay_pattern": rel["decay_rate"]
        }
    }
