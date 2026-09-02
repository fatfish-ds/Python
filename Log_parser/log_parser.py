import argparse
import re
from collections import defaultdict,Counter

#正则命名规则
failed = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) "
                    r"from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
                    )

def analyse(path:str, maxfailednum:int) -> None:
    failed_ip: Counter[str] = Counter()
    failed_users: dict[str,set[str]] = defaultdict(set)

    with open(path,"r",encoding="utf-8",errors="ignore") as handle:
        for line in handle:
            match = failed.search(line)
            if match:
                ip = match.group("ip")
                failed_ip[ip] += 1
                failed_users[ip].add(match.group("user"))

    offender = [(ip,n) for ip,n in failed_ip.most_common() if n >= maxfailednum]
    if not offender:
        print(f"没有攻击者")
        return
    print(f"{len(offender)} 个攻击者")
    for ip,n in offender:
        uses = ", ".join(sorted(failed_users[ip]))
        print(f"{ip}\t{n}\t{uses}")

def main() -> None:
    parser = argparse.ArgumentParser(description="日志分析")
    parser.add_argument("-p","--path",help="日志文件路径")
    parser.add_argument("-n","--num",type=int,help="最大失败的阈值",default=10)
    args = parser.parse_args()

    analyse(args.path,args.num)

if __name__ == "__main__":
    main()