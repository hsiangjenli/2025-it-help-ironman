from llm_guard.input_scanners import Secrets

prompt = "My password is P@ssw0rd123 and my API key is ABCD-1234-EFGH-5678-IJKL."

scanner = Secrets(redact_mode="REDACT_ALL")
sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

print("=" * 30)
print("Sanitized Prompt:", sanitized_prompt)
print("Is Valid:", is_valid)
print("Risk Score:", risk_score)
