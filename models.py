from dataclasses import dataclass, asdict
import json

@dataclass
class UsageRecord:
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    prompt_preview: str
    response_preview: str
    duration_ms: float

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
