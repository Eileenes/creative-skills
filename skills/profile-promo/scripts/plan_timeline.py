#!/usr/bin/env python3
"""Allocate a configurable story to integer frames using only the standard library.

Usage: python3 plan_timeline.py brief.json --out timeline.json
Frame intervals are [start_frame, end_frame); metadata on each beat is preserved.
"""

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


class PlanError(ValueError):
    """A brief cannot satisfy its timing constraints."""


def number(value, label, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise PlanError(f"{label} 必须为{'正' if positive else '非负'}数。")
    try:
        result = Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise PlanError(f"{label} 不是有效的有限数值。") from exc
    if result < 0 or (positive and result == 0):
        raise PlanError(f"{label} 必须为{'正' if positive else '非负'}数。")
    return result


def ceil(value):
    return -(-value.numerator // value.denominator)


def round_half_up(value):
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def plan(config):
    if not isinstance(config, dict):
        raise PlanError("输入必须为 JSON 对象。")
    duration = number(config.get("duration_seconds"), "duration_seconds", positive=True)
    fps = number(config.get("fps"), "fps", positive=True)
    total = round_half_up(duration * fps)
    if total < 1:
        raise PlanError("总时长不足 1 帧，请增加时长或帧率。")
    beats = config.get("beats")
    if not isinstance(beats, list) or not beats:
        raise PlanError("beats 必须为非空数组。")

    warnings = []

    def quantization(label, seconds, frames):
        if seconds * fps != frames:
            warnings.append(
                f"{label}: 请求 {float(seconds):.9g}s，量化为 {frames} 帧"
                f"（{float(Fraction(frames, 1) / fps):.9g}s）。"
            )

    quantization("总时长", duration, total)
    allocations, ceilings, weights, ids = [], [], [], set()
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            raise PlanError(f"beats[{index}] 必须为对象。")
        beat_id = beat.get("id")
        if not isinstance(beat_id, str) or not beat_id.strip() or beat_id in ids:
            raise PlanError(f"beats[{index}].id 必须是非空且唯一的字符串。")
        ids.add(beat_id)
        min_seconds = number(beat.get("min_seconds", 0), f"{beat_id}.min_seconds")
        minimum = max(1, ceil(min_seconds * fps))
        maximum = total
        if "min_seconds" in beat:
            quantization(f"{beat_id}.min_seconds", min_seconds, minimum)
        if "max_seconds" in beat:
            max_seconds = number(beat["max_seconds"], f"{beat_id}.max_seconds")
            maximum = (max_seconds * fps).__floor__()
            quantization(f"{beat_id}.max_seconds", max_seconds, maximum)
        if maximum < minimum:
            raise PlanError(f"{beat_id}: 上限不足以容纳下限（每拍至少 1 帧）。")
        weight = number(beat.get("weight", 1), f"{beat_id}.weight")
        if "fixed_seconds" in beat:
            seconds = number(beat["fixed_seconds"], f"{beat_id}.fixed_seconds", positive=True)
            fixed = round_half_up(seconds * fps)
            if not minimum <= fixed <= maximum:
                raise PlanError(f"{beat_id}: 固定时长与帧数上下限冲突。")
            quantization(f"{beat_id}.fixed_seconds", seconds, fixed)
            minimum = maximum = fixed
            weight = Fraction(0)
        allocations.append(minimum)
        ceilings.append(maximum)
        weights.append(weight)

    remaining = total - sum(allocations)
    if remaining < 0:
        raise PlanError(
            f"总预算 {total} 帧，小于固定时长与各拍下限之和 {sum(allocations)} 帧；"
            "请减少步骤、放宽约束或增加时长。"
        )

    # Weighted water filling: saturate bounded beats, then use largest remainders.
    # Ties follow input order, making the result independent of execution history.
    while remaining:
        active = [i for i in range(len(beats)) if weights[i] > 0 and allocations[i] < ceilings[i]]
        capacity = sum(ceilings[i] - allocations[i] for i in active)
        if capacity < remaining:
            raise PlanError(
                f"尚余 {remaining} 帧，但可伸缩节拍只能接收 {capacity} 帧；"
                "请提高 max_seconds、允许某拍 weight > 0，或缩短总时长。"
            )
        weight_sum = sum(weights[i] for i in active)
        quotas = {i: remaining * weights[i] / weight_sum for i in active}
        saturated = [i for i in active if quotas[i] >= ceilings[i] - allocations[i]]
        if saturated:
            for i in saturated:
                increment = ceilings[i] - allocations[i]
                allocations[i] += increment
                remaining -= increment
            continue
        floors = {i: quotas[i].__floor__() for i in active}
        for i in active:
            allocations[i] += floors[i]
            remaining -= floors[i]
        order = sorted(active, key=lambda i: (-(quotas[i] - floors[i]), i))
        for i in order[:remaining]:
            allocations[i] += 1
        remaining = 0

    result_beats, cursor = [], 0
    for beat, frames in zip(beats, allocations):
        result_beats.append({
            **beat,
            "start_frame": cursor,
            "end_frame": cursor + frames,
            "duration_frames": frames,
            "start_seconds": float(Fraction(cursor, 1) / fps),
            "end_seconds": float(Fraction(cursor + frames, 1) / fps),
            "duration_seconds": float(Fraction(frames, 1) / fps),
        })
        cursor += frames
    return {
        "requested_duration_seconds": float(duration),
        "duration_seconds": float(Fraction(total, 1) / fps),
        "total_frames": total,
        "fps": float(fps),
        "fps_fraction": str(fps),
        "interval_convention": "[start_frame, end_frame)",
        "beats": result_beats,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="包含 duration_seconds、fps、beats 的 JSON")
    parser.add_argument("--out", type=Path, help="省略时输出到 stdout")
    args = parser.parse_args()
    try:
        config = json.loads(args.brief.read_text(encoding="utf-8"))
        output = json.dumps(plan(config), ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (PlanError, OSError, ValueError) as exc:
        print(f"时间轴生成失败：{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
