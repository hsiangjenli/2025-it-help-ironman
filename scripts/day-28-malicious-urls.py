from llm_guard.output_scanners import MaliciousURLs

prompt = "Give me a list of interesting websites."
model_output = "Here is a link you might find interesting: http://malicious-website.com"

scanner = MaliciousURLs(threshold=0.7)
sanitized_output, is_valid, risk_score = scanner.scan(prompt, model_output)

print("=" * 30)
print("Sanitized Output:", sanitized_output)
print("Is Valid:", is_valid)
print("Risk Score:", risk_score)
