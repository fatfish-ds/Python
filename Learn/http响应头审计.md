## 脚本思路
1、预先设置需要检查的安全头，容易存在信息泄露的响应头

2、调用requests库，发起请求，并用函数收集信息

3、与预先设置好的检查项对比，得出结果，生成报告

---
## 运行结果

```text
200 OK https://www.sample.com/ {'Server': 'none', 'Date': 'Thu, 03 Sep 20xx 0x:xx:xx xxx', 'Content-Type': 'text/html', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Frame-Options': 'SAMEORIGIN, SAMEORIGIN', 'Frame-Options': 'SAMEORIGIN', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip'}

检查安全头

缺少的安全头Strict-Transport-Security: 强制使用HTTPS协议，防止中间人攻击（MITM）和SSL剥离

缺少的安全头Content-Security-Policy: 通过白名单缓解跨站脚本攻击和数据注入攻击

缺少的安全头X-Content-Type-Options: 阻止嗅探攻击（MIME），强制浏览器按照声明文件的类型处理文件

存在的安全头X-Frame-Options: SAMEORIGIN, SAMEORIGIN

缺少的安全头Referrer-Policy: 控制隐私的发送，不被透露到url或者浏览历史中，防止跨站脚本伪造（CSRF）

缺少的安全头Permissions-Policy: 限制敏感权限，防止脚本攻击滥用权限

检查敏感信息泄露头

危险头server: none

安全头缺少5个，存在危险头1个
```
以上数据为虚拟数据

---
## 总结
1、脚本忽视大小写问题，全部转化为小写再进行处理

2、能清晰看到缺少和存在的响应头，以及对应响应头的安全作用

3、脚本自动走完重定向链，到达最终的HTTPS页面

---
## 函数
1、.lower()将字母统一转化为小写

2、requests.get(allow_redirects=True)允许跟随重定向到最终页面

3、resp.status_code,  resp.headers,  resp.url等可以获取页面响应的信息
