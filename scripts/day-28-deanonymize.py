from llm_guard.output_scanners import Deanonymize
from llm_guard.vault import Vault

from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF

vault = Vault()
prompt = "My name is John Doe and I work at Test LLC."

scanner = Anonymize(
    vault,
    allowed_names=["John Doe"],
    hidden_names=["Test LLC"],
    recognizer_conf=BERT_LARGE_NER_CONF,
    language="en",
)
sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)
print("=" * 30)
model_output = f"This is a response to the prompt: {sanitized_prompt}"
print("Anonymized Model Output:", model_output)
scanner = Deanonymize(vault)
sanitized_model_output, is_valid, risk_score = scanner.scan(
    sanitized_prompt, model_output
)
print("Sanitized Model Output:", sanitized_model_output)
print("Is Valid:", is_valid)
print("Risk Score:", risk_score)
