from __future__ import annotations

import argparse
import sys

from chat_logic import DEFAULT_MODEL, DEFAULT_SYSTEM_PROMPT, generate_reply


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ollama와 통신하는 간단한 단일 턴 채팅 클라이언트"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"사용할 Ollama 모델 이름 (기본값: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--system",
        default=DEFAULT_SYSTEM_PROMPT,
        help="시스템 프롬프트 (기본값 사용 가능)",
    )
    parser.add_argument(
        "--user",
        required=True,
        help="유저 프롬프트",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        result = generate_reply(
            args.user,
            model=args.model,
            system_prompt=args.system,
        )
    except (RuntimeError, ValueError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    print("=== 모델 응답 ===")
    print(result.answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
