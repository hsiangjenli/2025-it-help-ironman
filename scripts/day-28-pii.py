from llm_guard.vault import Vault

from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF

vault = Vault()
prompt = "My name is John Doe and I work at Test LLC."

scanner = Anonymize(
    vault,
    recognizer_conf=BERT_LARGE_NER_CONF,
    language="en",
)
sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

print("="*30)
print("Sanitized Prompt:", sanitized_prompt)
print("Is Valid:", is_valid)
print("Risk Score:", risk_score)