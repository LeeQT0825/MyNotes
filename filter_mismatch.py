#!/usr/bin/env python3
"""筛选 prediction 与 reference 不一致的 detail，输出到新 JSON 文件。"""

import json
import sys
from pathlib import Path


def main():
    input_path = Path(__file__).parent / "test.json"
    output_path = Path(__file__).parent / "mismatches.json"

    if len(sys.argv) >= 2:
        input_path = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    details = data.get("details", {})
    if not isinstance(details, dict):
        print("错误: 'details' 不是对象")
        sys.exit(1)

    mismatches = {}
    for key, item in details.items():
        if not isinstance(item, dict):
            continue
        pred = item.get("prediction")
        ref = item.get("reference")
        if pred != ref:
            mismatches[key] = item

    result = {
        "total_mismatches": len(mismatches),
        "details": mismatches,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"共 {len(mismatches)} 条 prediction 与 reference 不一致，已写入: {output_path}")


if __name__ == "__main__":
    main()
