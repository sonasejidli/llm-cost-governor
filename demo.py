from dotenv import load_dotenv
from tracker.wrapper import TrackerWrapper
import sys, os
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set.")
    sys.exit(1)

tracker = TrackerWrapper()
system = {"role": "system", "content": "Sən Azərbaycan mütəxəssisisən. Cavabları Azərbaycan dilində və Azərbaycan reallıqlarına uyğun ver."}

suallar = ["Azərbaycanda ən hündür dağ hansıdır? ,Bakının neçə min əhalisi var? ,Azərbaycanın ən məşhur yeməkləri hansılardır?, Azərbaycanın ən məşhur idman növləri hansılardır?, Azərbaycanın ən məşhur musiqi növləri hansılardır?"]
for i, sual in enumerate(suallar):
    response = tracker.chat(
        messages=[
            system,
            {"role": "user", "content": sual}
        ]
    
    )

print(f"Sual {i+1}: {sual}")
print(f"Cavab: {response.choices[0].message.content}")
print("Token logu yazildi: data/usage.db")
