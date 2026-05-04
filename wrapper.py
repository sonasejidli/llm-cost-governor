import time
from datetime import datetime
from openai import OpenAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracker.models import UsageRecord
from tracker.storage import StorageManager
from tracker.budget import check_budget
from tracker.router import select_model

class TrackerWrapper:
    def __init__(self, api_key: str = None, auto_route: bool = True):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be provided")
        self.client = OpenAI(api_key=api_key)
        self.storage = StorageManager()
        self.auto_route = auto_route

    def chat(self, messages: list, model: str = None, **kwargs):
        budget = check_budget()
        print(f"[Budget] {budget['message']}")

        if budget["status"] == "hard_stop":
            raise Exception(f"API çağırışı bloklandı: {budget['message']}")

        prompt = messages[-1].get("content", "") if messages else ""

        if model is None and self.auto_route:
            route = select_model(prompt)
            model = route["model"]
            print(f"[Router] {route['reason']}")
        elif model is None:
            model = "gpt-4o-mini"

        start = time.time()
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        duration_ms = (time.time() - start) * 1000
        input_tokens  = getattr(response.usage, "prompt_tokens", 0)
        output_tokens = getattr(response.usage, "completion_tokens", 0)
        record = UsageRecord(
            timestamp=datetime.utcnow().isoformat(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            prompt_preview=prompt[:80],
            response_preview=getattr(response.choices[0].message, "content", "")[:80],
            duration_ms=round(duration_ms, 2)
        )
        self.storage.save(record)
        return response
