import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置超时时间
socket.setdefaulttimeout(2.0)
# 解析域名为ip地址
def resolve(dns: str) -> tuple[str, list[str]]:
    try:
        _, _, ips = socket.gethostbyname_ex(dns)
        return dns, ips
    except socket.gaierror:
        return dns, []
# 并发解析
def dns_subs(domain: str, words: list[str], workers: int) -> None:
    candidates = [f"{w.strip()}.{domain}" for w in words if w.strip()]
    found = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(resolve,dns) for dns in candidates]
        for future in as_completed(futures):
            dns, ips = future.result()
            if ips:
                found += 1
                print(f"{dns:<32} {'--'.join(ips)}")
    print(f"found: {found}")

def main():
    parser = argparse.ArgumentParser(description="domain enumerator")
    parser.add_argument("domain", help="domain to enumerate")
    parser.add_argument("--words", "-w", help="words to enumerate")
    parser.add_argument("--workers",type=int,default=50, help="number of workers")
    args = parser.parse_args()

    with open(args.words,encoding="utf-8",errors="ignore") as handle:
        words = handle.read().splitlines()
    dns_subs(args.domain, words, args.workers)

if __name__ == "__main__":
    main()