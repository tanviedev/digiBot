"""

from engine.loader import load_json

content = load_json("data/content_metadata.json")
performance = load_json("data/performance_metrics.json")

# simplified demo
results = []

for post in performance:
    result = {
        "content_id": post["content_id"],
        "status": "processed"
    }
    results.append(result)

print(results)

"""
from engine.load_all_data import load_all
from engine.base_engine import run_base_engine
import json

data = load_all()

content_id = "cnt_007"  # try changing this

output = run_base_engine(content_id, data)

print(json.dumps(output, indent=2))
