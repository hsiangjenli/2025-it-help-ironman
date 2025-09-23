# 介紹

# 操作

```shell
docker run -d --name mcpgateway \
  --network=host \
  -e MCPGATEWAY_UI_ENABLED=true \
  -e MCPGATEWAY_ADMIN_API_ENABLED=true \
  -e HOST=0.0.0.0 \
  -e PORT=4444 \
  -e MCPGATEWAY_A2A_ENABLED=true \
  -e MCPGATEWAY_A2A_METRICS_ENABLED=true \
  -v $(pwd)/data:/data \
  ghcr.io/ibm/mcp-context-forge:0.6.0
```

# 重點回顧

# 參考資料