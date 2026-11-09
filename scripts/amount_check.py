#!/usr/bin/env python3
"""回款助手 · 金额工具：人民币大写转换 + 报价勾稽校验。

用法：
  python3 amount_check.py to-rmb-caps 3600
  python3 amount_check.py check --items 800,1200 --deposit-rate 0.5 --paid 1000
"""
import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP

DIGITS = "零壹贰叁肆伍陆柒捌玖"
UNITS = ["", "拾", "佰", "仟"]
BIG_UNITS = ["", "万", "亿", "兆"]


def to_rmb_caps(amount) -> str:
    """把金额（元，可带小数）转成人民币大写，如 3600 -> 叁仟陆佰元整。"""
    d = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if d < 0:
        raise ValueError("金额不能为负")
    integer = int(d)
    cents = int((d - integer) * 100)
    if integer == 0:
        result = "零元"
    else:
        groups = []
        n = integer
        while n:
            groups.append(n % 10000)
            n //= 10000
        parts = []
        for gi in range(len(groups) - 1, -1, -1):
            g = groups[gi]
            if g == 0:
                if parts and not parts[-1].endswith("零"):
                    parts.append("零")
                continue
            seg = ""
            zero_pending = False
            for pos in range(3, -1, -1):
                digit = (g // (10 ** pos)) % 10
                if digit == 0:
                    zero_pending = True
                else:
                    if zero_pending and seg:
                        seg += "零"
                    zero_pending = False
                    seg += DIGITS[digit] + UNITS[pos]
            parts.append(seg + BIG_UNITS[gi])
        result = "".join(parts).rstrip("零") + "元"
    jiao, fen = cents // 10, cents % 10
    if jiao == 0 and fen == 0:
        return result + "整"
    tail = ""
    if jiao:
        tail += DIGITS[jiao] + "角"
    if fen:
        if not jiao:
            tail += "零"
        tail += DIGITS[fen] + "分"
    return result + tail


def check(items, deposit_rate, paid):
    total = sum(Decimal(str(x)) for x in items)
    deposit = (total * Decimal(str(deposit_rate))).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    balance = total - deposit
    paid_d = Decimal(str(paid))
    ok = paid_d <= total
    print(f"明细合计：¥{total:.2f}（人民币{to_rmb_caps(total)}）")
    print(f"定金（{deposit_rate}）：¥{deposit:.2f}　尾款：¥{balance:.2f}")
    print(f"定金+尾款 = 合计：{deposit + balance == total}")
    print(f"已收：¥{paid_d:.2f}　未收：¥{total - paid_d:.2f}　已收不超过应收：{ok}")
    return 0 if ok and deposit + balance == total else 1


def main():
    p = argparse.ArgumentParser(description="回款助手金额工具")
    sub = p.add_subparsers(dest="cmd", required=True)
    c1 = sub.add_parser("to-rmb-caps")
    c1.add_argument("amount")
    c2 = sub.add_parser("check")
    c2.add_argument("--items", required=True, help="逗号分隔的小计，如 800,1200")
    c2.add_argument("--deposit-rate", default="0.3")
    c2.add_argument("--paid", default="0")
    args = p.parse_args()
    if args.cmd == "to-rmb-caps":
        print(to_rmb_caps(args.amount))
        return 0
    items = [x.strip() for x in args.items.split(",") if x.strip()]
    return check(items, args.deposit_rate, args.paid)


if __name__ == "__main__":
    sys.exit(main())
