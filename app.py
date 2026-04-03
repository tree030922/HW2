import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Change this prompt if you want to test a different style.
PROMPT = "Write a short, catchy social media caption for this product."

MODEL = "gemini-2.5-flash"


def call_gemini(api_key, product_description):
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            f"{PROMPT}\n\n"
                            f"Product Description:\n{product_description}\n\n"
                            "Return only the social caption text."
                        )
                    }
                ]
            }
        ]
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_caption(response_json):
    return response_json["candidates"][0]["content"]["parts"][0]["text"].strip()


def main():
    parser = argparse.ArgumentParser(description="Simple Gemini homework script")
    parser.add_argument("product_description", help="Product description text")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is missing.", file=sys.stderr)
        print("Example: export GEMINI_API_KEY='your_key_here'", file=sys.stderr)
        return 1

    try:
        response_json = call_gemini(api_key, args.product_description)
        caption = extract_caption(response_json)
    except urllib.error.HTTPError as e:
        error_text = e.read().decode("utf-8", errors="ignore")
        print(f"API request failed: {e.code}", file=sys.stderr)
        print(error_text, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print("=== Product Description ===")
    print(args.product_description)
    print()
    print("=== Social Caption ===")
    print(caption)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
