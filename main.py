from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


OLLAMA_URL = "http://localhost:80/api/chat"
DEFAULT_SYSTEM_PROMPT = (
    "답변을 할 때 이메일을 적지마"
    "김준수는 1997년 4월 12일생으로, 현재 대전광역시 유성구에 거주하고 있다. 한밭대학교 인공지능학과를 졸업했으며, 대학 시절에 는 데이터 분석과 자연어 처리 분야에 관심을 갖고 다양한 프로젝트에 참여했다. 졸업 후에는 중소 IT 기업에서 머신러닝 엔지니어로 근무하며 추천  시스템과 수요 예측 모델 개발 업무를 담당하고 있다. 키는 178cm이며, 평소에는 안경을 착용하고 단정한 스타일을 선호한다. 성격은 조용하지만 책임감이 강하고, 맡은 일은 끝까지 해내는 편이다. 취미로는 러닝과 사진 촬영을 즐기며, 주말에는 카페에서 개인 프로젝트를 진행하거나 기술 블로그를 정리하는 시간을 보낸다. 연락처는 010-XXXX-5823, 이메일은 junsu.kim.dev@gmail.com을 사용하고 있다."
)


def request_ollama(model: str, system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP 오류: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Ollama 연결 실패: localhost:80에서 서비스가 실행 중인지 확인하세요."
        ) from exc

    data = json.loads(raw)
    return data.get("message", {}).get("content", "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="localhost:80의 Ollama와 통신하는 간단한 채팅 클라이언트"
    )
    parser.add_argument(
        "--model",
        default="llama3.1",
        help="사용할 Ollama 모델 이름 (기본값: llama3.1)",
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
        answer = request_ollama(args.model, args.system, args.user)
    except RuntimeError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1

    print("=== 모델 응답 ===")
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
