"""Interactive terminal CLI to query the Urban Rooftop Organic Farming Assistant."""

import sys
import asyncio
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.rag_chain import run_rag_pipeline
from app.config import get_settings


async def main():
    """Interactive loop for CLI questions."""
    print("=" * 75)
    print("🌿 Urban Rooftop Organic Farming Assistant - Terminal Query CLI")
    print("=" * 75)
    print("Type your rooftop agronomy question below (or type 'exit' / 'quit' to stop).\n")

    settings = get_settings()

    while True:
        try:
            query = input("\n🧑‍🌾 Your Question: ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                print("\nGoodbye and happy organic farming! 🌿")
                break

            print("\n🔍 Retrieving context from Pinecone and generating answer via Gemini...")
            answer, sources, chunk_count, model_used, latency_ms = await run_rag_pipeline(
                question=query
            )

            print("\n" + "=" * 75)
            print("🌱 Verified Agronomic Advice:")
            print("=" * 75)
            print(answer)
            print("-" * 75)
            print(f"📊 Latency: {latency_ms:.2f}ms | Model: {model_used} | Retrieved Chunks: {chunk_count}")

            if sources:
                print("\n📚 Grounded Sources:")
                for i, src in enumerate(sources, 1):
                    print(f" [{i}] {src.title} ({src.source})")
                    print(f"     Excerpt: {src.content_snippet[:120]}...\n")
            print("=" * 75)

        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break
        except Exception as e:
            print(f"\n❌ Error during execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
