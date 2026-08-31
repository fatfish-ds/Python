import argparse
import hashlib
import re

by_length = {
    32:["md5","ntlm"],
    40:["sha1"],
    56:["sha224"],
    64:["sha256"],
    96:["sha384"],
    128:["sha512"],
}
HEX = re.compile(r"^[0-9a-fA-F]+$")
ALGOS = {name:name for name in ("md5","sha1","sha256","sha384","sha512")}

# 识别算法
def identify(h: str) -> list[str]:
    h = h.strip()
    if not HEX.match(h):
        return []
    return by_length.get(len(h), [])
#计算哈希值
def digest(word: str,algo:str) -> str:
    return hashlib.new(algo,word.encode()).hexdigest()
#密码变形生成
def mangle(word: str):
    yield word
    yield word.capitalize()
    yield word + "1"
    yield word + "123"
    yield word + "?"
    yield word + "!"
    yield word.replace("o","0").replace("e","3")
#暴力破解
def crack(target:str,wordlist:str,algos:list[str]) -> None:
    target = target.strip().lower()
    print(f"候选算法列表：{', '.join(algos) or '未知'}\n")
    tried = 0
    with open(wordlist,encoding="utf-8",errors="ignore") as f:
        for line in f:
            line1 = line.rstrip("\n")
            for candidate in mangle(line1):
                for algo in algos:
                    if algo not in ALGOS:
                        continue
                    tried += 1
                    if digest(candidate,algo) == target:
                        print(f"用{algo}破解了{candidate}\nf”尝试了{tried}次")
                        return
    print(f"not found after {tried} tries\n")
#命令行
def main() -> None:
    parser = argparse.ArgumentParser(description="哈希算法识别和破解")
    parser.add_argument("hash",help="指定的哈希值")
    parser.add_argument("-w","--wordlist",default="words.txt")
    parser.add_argument("-a","--algo",help="选择哈希算法")
    args = parser.parse_args()

    algos = [args.algo] if args.algo else identify(args.hash)
    if not algos:
        print(f"无法识别到算法类型")
        return
    crack(args.hash,args.wordlist,algos)

if __name__ == "__main__":
    main()