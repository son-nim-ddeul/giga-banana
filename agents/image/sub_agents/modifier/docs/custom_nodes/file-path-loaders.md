# 파일 경로·로더

**패키지:** ComfyUI-EasyFilePaths  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md)

---

## Easy Checkpoint Loader
- 입력: ckpt_hint (STRING)
- 출력: MODEL, CLIP, VAE, ckpt_full_path
- widgets_values: `["cyberrealistic"]` (힌트만, 정확/끝/부분 일치)

**사용 상황**
1. 체크포인트 파일명이 길어 전체 입력이 번거로울 때 (힌트만으로 자동 매칭)
2. 같은 계열 모델 여러 버전(예: v1, v2)을 스크립트/자동화에서 전환할 때
3. 외부 시스템에서 "cyberrealistic"처럼 짧은 식별자만 넘겨받을 때
4. 워크플로우를 다른 환경으로 옮길 때 로컬 경로/파일명 차이를 흡수하고 싶을 때
5. A/B 테스트로 서로 다른 체크포인트를 힌트만 바꿔 빠르게 비교할 때

---

## Easy LoRA Loader
- 입력: model(MODEL), lora_hint(STRING), strength_model(FLOAT)
- 출력: MODEL, lora_full_path
- widgets_values: `["pixel", 0.8]`

**사용 상황**
1. LoRA 파일명 일부(예: pixel_art)만 알고 있을 때
2. 여러 LoRA 중 이름 패턴으로 하나를 골라 쓸 때
3. 배치/자동화에서 LoRA 이름을 짧은 힌트로만 지정하고 싶을 때
4. 동일 스타일 LoRA가 버전별로 여러 개 있을 때 힌트로 버전 전환
5. 외부 API/설정에서 LoRA를 "pixel" 같은 키로만 지정받을 때

---

## Easy VAE Loader / CLIP Loader / UNET Loader
- VAE: vae_hint → VAE, vae_full_path. 위젯 vae_hint (예: sdxl_vae)
- CLIP/UNET 동일 힌트 패턴

**사용 상황**
1. VAE/CLIP 파일명을 정확히 모르고 키워드만 알고 있을 때
2. SD/SDXL 등 여러 VAE를 환경별로 힌트만 바꿔 쓰고 싶을 때
3. 체크포인트와 별도 VAE를 "sdxl", "ema" 같은 짧은 이름으로 지정할 때
4. 자동화 스크립트에서 VAE/CLIP를 문자열 하나로 선택하고 싶을 때
5. 여러 프로젝트에서 공통 VAE를 힌트로만 참조해 경로 차이를 줄일 때

---

## Character LoRA Select
- 입력 없음(위젯 캐릭터 선택). 출력: lora_sdxl, power_sdxl, lora_qwen, power_qwen, lora_chroma, power_chroma, character_prompt, character_name
- 설정: configs/character_config.json

**사용 상황**
1. 웹툰/일러스트에서 캐릭터별로 고정 LoRA+프롬프트를 쓰고 싶을 때
2. 여러 캐릭터를 한 워크플로우에서 드롭다운으로 전환하고 싶을 때
3. 캐릭터별 최적 강도·트리거 워드를 config에서 한 번에 관리하고 싶을 때
4. 팀/프로젝트에서 캐릭터 설정을 JSON으로 공유하고 싶을 때
5. 동일 캐릭터를 SDXL/Qwen/Chroma 등 여러 모델에 맞춰 쓸 때
6. 일관된 캐릭터 연출을 여러 장에 반복 적용할 때
7. 스토리/에피소드별로 캐릭터 세트를 바꾸고 싶을 때
8. LoRA+프롬프트를 코드가 아닌 설정 파일로만 바꾸고 싶을 때
9. A/B 테스트로 캐릭터별 설정을 빠르게 전환할 때
10. 외부 툴에서 "캐릭터 ID"만 넘기고 LoRA/프롬프트는 노드에서 매핑하고 싶을 때

---

## Easy File Name
- 입력 없음. 출력: relative_path, absolute_path, user. 위젯 story_path, user_name

**사용 상황**
1. 스토리/에피소드 단위로 저장 경로를 나누고 싶을 때
2. 사용자(작가)별로 출력 폴더를 분리하고 싶을 때
3. Image Saver 등에 동적 경로(relative_path, user)를 넘기고 싶을 때
4. 배치 작업에서 스토리 ID·사용자명을 파일명/경로에 포함하고 싶을 때
5. 로컬과 서버에서 경로 규칙만 맞추고 실제 경로는 노드에 맡기고 싶을 때

---

## Easy JSON Job Tracker
- 입력: job_file(STRING), mode(COMBO). 출력: job_data, job_id
- mode: get_next, mark_done, add_job. 위젯 `["jobs.json", "get_next"]`

**사용 상황**
1. 대기열(큐)에 쌓인 작업을 하나씩 꺼내 실행하고 싶을 때
2. 외부 스크립트/API가 JSON 파일로 작업을 추가하고 ComfyUI가 소비하고 싶을 때
3. 배치 생성 시 작업 완료/실패를 JSON에 반영해 추적하고 싶을 때
4. 여러 ComfyUI 인스턴스가 같은 job 파일을 보고 순서대로 처리하고 싶을 때
5. 재시작 후에도 남은 작업만 이어서 처리하고 싶을 때
6. 작업 ID를 파일명/메타데이터에 넣어 나중에 추적하고 싶을 때
7. get_next → 실행 → mark_done 흐름으로 자동화 파이프라인을 만들고 싶을 때
8. add_job으로 웹/CLI에서 작업만 넣고 워크플로우는 동일하게 돌리고 싶을 때
9. 작업별 프롬프트·설정을 job_data로 넘기고 싶을 때
10. 실험/테스트용으로 로컬 JSON 파일만으로 간단한 큐를 쓰고 싶을 때
