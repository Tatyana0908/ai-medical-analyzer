import json
import requests
import time
import csv

API_URL = "http://127.0.0.1:8000/analyze"


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_api(sample):
    payload = {
        "test_name": sample["test_name"],
        "values": sample["values"],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def run_evaluation(dataset):
    results = []

    for sample in dataset:
        result = call_api(sample)

        results.append({
            "request": sample,
            "response": result
        })

        time.sleep(0.5)

    return results


def save_results(results, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def save_csv(results, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["запрос", "результат"])

        for r in results:
            writer.writerow([
                json.dumps(r["request"], ensure_ascii=False),
                json.dumps(r["response"], ensure_ascii=False)
            ])

if __name__ == "__main__":
    dataset = load_dataset("../data/test_dataset.json")
    results = run_evaluation(dataset)
    save_results(results, "../eval/results.json")
    save_csv(results, "../eval/results.csv")
