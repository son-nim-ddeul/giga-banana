# 메타데이터·저장

**패키지:** comfyui-image-saver, comfyui-lora-manager, ComfyUI-EasyFilePaths  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## Image Saver
- 입력: images(IMAGE), filename(STRING), path(STRING), extension(STRING), steps, cfg, modelname, sampler_name, scheduler, positive, negative, seed_value, width, height, lossless_webp, quality_jpeg_or_webp, counter, time_format
- 파일명 플레이스홀더: %date%, %time%, %model%, %steps%, %cfg%, %seed%, %counter%, %width%, %height%. 예: `output_%date%_%time%_%model%_s%steps%_seed%seed%_%counter%`

**사용 상황**
1. 생성 파라미터(모델, 스텝, 시드)를 파일명에 넣어 나중에 재현하고 싶을 때
2. %date%, %time%으로 실행 시각별로 폴더/파일을 나누고 싶을 때
3. %counter%로 자동 증가 번호를 붙이고 싶을 때
4. PNG에 ComfyUI 워크플로우+A1111 스타일 메타데이터를 넣고 싶을 때
5. Input Parameters (Image Saver)와 연결해 스텝/CFG/샘플러 등을 메타데이터로 남기고 싶을 때
6. path를 Easy File Name 등에서 받아 사용자/스토리별로 저장하고 싶을 때
7. extension을 png/jpg/webp로 바꿔 포맷만 선택하고 싶을 때
8. lossless_webp, quality로 웹용 용량/품질을 조절하고 싶을 때
9. 배치 저장 시 파일명이 겹치지 않게 플레이스홀더로 구분하고 싶을 때
10. 외부 툴에서 메타데이터를 읽어 재현/추가 처리하고 싶을 때

---

## Input Parameters (Image Saver)
- 입력: steps, cfg, sampler_name, scheduler, denoise, seed(INT). 출력: METADATA → Image Saver 등에 연결

**사용 상황**
1. KSampler 등에서 쓰인 steps, cfg, seed를 Image Saver에 넘기고 싶을 때
2. 파일명/메타데이터에 "어떤 설정으로 생성했는지" 포함하고 싶을 때
3. 재현용으로 모든 샘플링 파라미터를 한 노드로 모아 저장하고 싶을 때
4. Image Saver의 filename 플레이스홀더가 %steps%, %seed% 등을 쓸 수 있게 하고 싶을 때
5. 메타데이터 기반 검색/필터를 위해 PNG 등에 파라미터를 넣고 싶을 때
6. A/B 테스트 결과를 설정별로 구분해 저장하고 싶을 때
7. 워크플로우에서 "설정 수집"을 한 노드로 표현하고 싶을 때
8. Save Image LM 등과 함께 LoRA 정보 외에 샘플링 정보도 남기고 싶을 때
9. 배치별로 다른 steps/cfg를 썼을 때 파일명에 반영하고 싶을 때
10. 나중에 동일 설정으로 재실행할 수 있게 메타데이터를 남기고 싶을 때

---

## Save Image LM
- 입력: images(IMAGE), filename(STRING), lora_info(STRING). LoRA 정보 메타데이터 포함 저장

**사용 상황**
1. 사용한 LoRA 이름·강도를 이미지 메타데이터에 남기고 싶을 때
2. Lora Loader (LoraManager)의 loaded_loras 등을 lora_info로 넘기고 싶을 때
3. 재현 시 "어떤 LoRA를 썼는지" 메타데이터에서 읽고 싶을 때
4. LoRA 중심 워크플로우에서 저장 시 항상 LoRA 정보를 포함하고 싶을 때
5. 캐릭터/스타일 LoRA 조합을 파일별로 기록하고 싶을 때
6. A1111 호환 메타데이터로 LoRA 정보를 남기고 싶을 때
7. 배치 저장 시 각 이미지별 LoRA 정보를 남기고 싶을 때
8. Image Saver + Input Parameters와 함께 "전체 설정+LoRA"를 한 번에 남기고 싶을 때
9. 외부 툴에서 메타데이터만 파싱해 LoRA 목록을 추출하고 싶을 때
10. 실험 로그/버전 관리에서 LoRA 설정을 추적하고 싶을 때

---

## Easy JSON Job Tracker
- 입력: job_file(STRING), mode(COMBO). 출력: job_data, job_id. mode: get_next, mark_done, add_job

**사용 상황**
1. 대기열(큐)에서 다음 작업을 꺼내 실행하고 싶을 때 (get_next)
2. 작업 완료/실패를 JSON에 반영하고 싶을 때 (mark_done)
3. 외부 스크립트/API가 JSON 파일로 작업을 추가하고 싶을 때 (add_job)
4. ComfyUI를 재시작해도 남은 작업만 이어서 처리하고 싶을 때
5. 여러 ComfyUI 인스턴스가 같은 job 파일을 보고 순서대로 처리하고 싶을 때
6. job_data에 프롬프트/설정을 넣어 워크플로우에 전달하고 싶을 때
7. job_id를 파일명/메타데이터에 넣어 추적하고 싶을 때
8. 배치 자동화 파이프라인에서 "작업 추가 → 실행 → 완료 표시" 흐름을 만들고 싶을 때
9. 웹/CLI에서 작업만 넣고 워크플로우는 동일하게 돌리고 싶을 때
10. 실험/테스트용으로 로컬 JSON 파일만으로 간단한 큐를 쓰고 싶을 때
