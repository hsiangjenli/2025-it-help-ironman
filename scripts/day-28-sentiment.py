from llm_guard.input_scanners import Sentiment

prompt_neg = "I hate programming and solving problems!"
prompt_pos = "I love programming and solving problems!"

scanner = Sentiment(threshold=0)
sanitized_prompt_neg, is_valid_neg, risk_score_neg = scanner.scan(prompt_neg)
sanitized_prompt_pos, is_valid_pos, risk_score_pos = scanner.scan(prompt_pos)
print("=" * 30)
print("Sanitized Prompt (Negative):", sanitized_prompt_neg)
print("Is Valid (Negative):", is_valid_neg)
print("Risk Score (Negative):", risk_score_neg)
print("=" * 30)
print("Sanitized Prompt (Positive):", sanitized_prompt_pos)
print("Is Valid (Positive):", is_valid_pos)
print("Risk Score (Positive):", risk_score_pos)
