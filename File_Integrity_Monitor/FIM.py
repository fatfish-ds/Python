import hashlib
from pathlib import Path
import argparse
import json

CHUNK_SIZE = 65536
#计算文件哈希值
def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda:handle.read(CHUNK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()
#生成关系字典
def snapshot(root: Path) -> dict[str, str] :
    state: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            state[str(path.relative_to(root))] = file_sha256(path)
    return state

def baseline(root: Path,db: Path) -> None:
    temp = snapshot(root)
    db.write_text(json.dumps(temp,indent=2))
    print(f"baseline {len(temp)} files -> {db}")

def check(root: Path,db: Path) -> None:
    if not db.exists():
        print(f"没有关系文件，请检查基准文件是否存在")
        return
    old = json.loads(db.read_text())
    new = snapshot(root)

    add = sorted(set(new) - set(old))
    remove = sorted(set(old) - set(new))
    change = sorted(f for f in set(old) & set(new) if old[f] != new[f])

    if not (add or remove or change):
        print(f"没有变化")
        return

    for f in add:
        print(f"增加了{f}")
    for f in remove:
        print(f"减少了{f}")
    for f in change:
        print(f"{f}改变了")

def main() -> None:
    parser = argparse.ArgumentParser(description="文件完整性检测")
    parser.add_argument("-choose",choices=["baseline","check"])
    parser.add_argument("-root",help="要监管的文件")
    parser.add_argument("-db",default="baseline.json",help="基准文件")
    args = parser.parse_args()

    root ,db = Path(args.root),Path(args.db)
    if args.choose == "baseline":
        baseline(root,db)
    else:
        check(root,db)

if __name__ == "__main__":
    main()