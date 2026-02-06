from engine.load_all_data import load_all
from engine.base_engine import run_base_engine
import json


def run_for_all(test_content_ids=None):
    """
    If test_content_ids is provided (list),
    only those content_ids will be processed.
    """
    data = load_all()
    results = []

    all_content_ids = data["performance"].keys()

    for content_id in all_content_ids:
        # --- TEST MODE FILTER ---
        if test_content_ids and content_id not in test_content_ids:
            continue

        try:
            output = run_base_engine(content_id, data)
            results.append(output)
        except Exception as e:
            print(f"Failed for {content_id}: {e}")

    return results


if __name__ == "__main__":
    # 👇 CHANGE THIS LIST TO TEST FEW CONTENTS
    TEST_CONTENT_IDS = ["cnt_001", "cnt_002"]
    # TEST_CONTENT_IDS = None  # ← uncomment this to run ALL later

    engine_outputs = run_for_all(TEST_CONTENT_IDS)

    with open("outputs/base_engine_outputs.json", "w") as f:
        json.dump(engine_outputs, f, indent=2)

    print(f"Generated outputs for {len(engine_outputs)} posts")
