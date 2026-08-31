import argparse
import math
import secrets
import string

EASY_PWD = {"123456","password","admin","iloveoyou","123456789","qwerty"}

SETS = {
    "LOWER":string.ascii_lowercase,
    "UPPER":string.ascii_uppercase,
    "digits":string.digits,
    "symbols":"!@#$%^&*()_+-={}:><][;'/.,'"
}

def generate_password(length: int = 16) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4")
    pools = list(SETS.values())
    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

def entropy_bits(password: str) -> float:
    pool = 0
    if any(c in SETS["LOWER"] for c in password):
        pool += 26
    if any(c in SETS["UPPER"] for c in password):
        pool += 26
    if any(c in SETS["digits"] for c in password):
        pool += 10
    if any(c in SETS["symbols"] for c in password):
        pool += len(SETS["symbols"])
    return len(password) * math.log2(pool) if pool else 0.0

def rate(password: str) -> str:
    if password.lower() in EASY_PWD:
        return "week password"
    bits = entropy_bits(password)
    if bits < 40:
        verdict = "very weak"
    elif bits < 60:
        verdict = "medium"
    elif bits < 80:
        verdict = "strong"
    else:
        verdict = "very strong"
    return f"{verdict} (~{bits:.0f} bits)"

def main() -> None:
    parser = argparse.ArgumentParser(description="选择生成或者检查")
    sub = parser.add_subparsers(dest="cmd",required=True)
    gen = sub.add_parser("gen",help="generate password")
    gen.add_argument("--length","-1",type=int,default=16)
    chk = sub.add_parser("check",help="check password")
    chk.add_argument("password")
    args = parser.parse_args()
    if args.cmd == "gen":
        pw = generate_password(args.length)
        print(f"{pw} -> {rate(pw)}")
    else:
        print(rate(args.password))

if __name__ == "__main__":
    main()