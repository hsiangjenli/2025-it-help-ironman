# 介紹

# 操作

```shell
docker run -d --name mcpgateway \
  -p 4444:4444 \
  -e MCPGATEWAY_UI_ENABLED=true \
  -e MCPGATEWAY_ADMIN_API_ENABLED=true \
  -e HOST=0.0.0.0 \
  -e PORT=4444 \
  -e MCPGATEWAY_A2A_ENABLED=true \
  -e MCPGATEWAY_A2A_METRICS_ENABLED=true \
  -v $(pwd)/data:/data \
  ghcr.io/ibm/mcp-context-forge:0.6.0
```

![20250923235945](https://raw.githubusercontent.com/hsiangjenli/pic-bed/main/images/20250923235945.png)

> **補充說明**
>
> 因為在 Mac 上要讓容器內的服務可以存取主機的網路，必須使用[ `http://host.docker.internal:10000`](http://host.docker.internal:10000) 來存取主機的服務

# 重點回顧

# 參考資料