#!/usr/bin/env python3
"""
簡單的 A2A 測試腳本，包含超時處理
"""
import asyncio
import httpx
import json
from uuid import uuid4

async def test_agent_with_timeout():
    """測試 A2A 代理，包含超時處理"""
    
    # 設定較長的超時時間
    timeout = httpx.Timeout(200.0, connect=10.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        payload = {
            "id": str(uuid4()),
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "message": {
                    "kind": "message",
                    "messageId": str(uuid4()),
                    "parts": [
                        {
                            "kind": "text",
                            "text": "How much is 10 USD in EUR?"
                        }
                    ],
                    "role": "user"
                }
            }
        }
        
        try:
            print("🚀 發送請求到 A2A 伺服器...")
            print(f"📝 請求內容: {json.dumps(payload, indent=2)}")
            
            response = await client.post(
                "http://localhost:10000",
                json=payload
            )
            
            print(f"✅ 收到回應 (狀態碼: {response.status_code})")
            response_data = response.json()
            print(f"📄 回應內容: {json.dumps(response_data, indent=2)}")
            
            if "error" in response_data:
                print(f"❌ 伺服器錯誤: {response_data['error']}")
            else:
                print("🎉 請求成功!")
                
        except httpx.TimeoutException:
            print("⏰ 請求超時!")
        except Exception as e:
            print(f"💥 發生錯誤: {e}")

if __name__ == "__main__":
    print("🧪 開始測試 A2A 代理 (含超時處理)")
    asyncio.run(test_agent_with_timeout())