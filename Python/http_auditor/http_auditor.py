import requests
import sys
import argparse

# 希望出现的响应头
EXPECTED = {
    "Strict-Transport-Security": "强制使用HTTPS协议，防止中间人攻击（MITM）和SSL剥离",
    "Content-Security-Policy": "通过白名单缓解跨站脚本攻击和数据注入攻击",
    "X-Content-Type-Options": "阻止嗅探攻击（MIME），强制浏览器按照声明文件的类型处理文件",
    "X-Frame-Options": "防止点击劫持，不允许网站被嵌入到框架中",
    "Referrer-Policy": "控制隐私的发送，不被透露到url或者浏览历史中，防止跨站脚本伪造（CSRF）",
    "Permissions-Policy": "限制敏感权限，防止脚本攻击滥用权限",
}
# 一些敏感信息泄露头
LEAKY=["server","X-powered-By","X-AspNet-Version","X-Generator"]

def audit(url: str, timeout: float= 10.0) -> int:
    try:
        resp = requests.get(url, timeout=timeout, allow_redirects=True)
    except requests.RequestException as e:
        print(e)
        return 2
    print(f"{resp.status_code} {resp.reason} {resp.url} {resp.headers}\n")
    headers = {k.lower(): v for k, v in resp.headers.items()}

    print("检查安全头")
    missing = 0
    for k, v in EXPECTED.items():
        if k.lower() in headers:
            print(f"存在的安全头{k}: {headers[k.lower()]}")
        else:
            missing+=1
            print(f"缺少的安全头{k}: {v}")

    print("\n检查敏感信息泄露头")
    leaks = 0
    for k in LEAKY:
        if k.lower() in headers:
            leaks += 1
            print(f"危险头{k}: {headers[k.lower()]}")
        if not leaks:
            print(f"没有危险头")

    print(f"安全头缺少{missing}个，存在危险头{leaks}个")
    return 1 if (missing or leaks) else 0

def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP审计")
    parser.add_argument("-u","--url",help="审计url")
    args = parser.parse_args()
    sys.exit(audit(args.url))

if __name__ == "__main__":
    main()