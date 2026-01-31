# LoRA

**패키지:** comfyui-lora-manager, rgthree-comfy  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md)

---

## Lora Loader (LoraManager)
- 입력: model(MODEL), text(STRING), clip(CLIP), lora_stack(LORA_STACK 선택)
- 출력: MODEL, CLIP, trigger_words, loaded_loras
- text 형식: `<lora:이름:강도>` 또는 `<lora:이름:model_str:clip_str>`. 여러 개 공백 구분
- widgets_values: `["<lora:pixel_art:0.8> <lora:anime:1.0>"]`

**사용 상황**
1. 프롬프트와 LoRA를 한 문자열로 관리하고 싶을 때 (A1111 스타일)
2. 외부 시스템/API에서 `<lora:이름:강도>` 형식만 넘겨받을 때
3. 여러 LoRA를 한 번에 로드하고 트리거 워드를 자동 추출해 프롬프트에 붙이고 싶을 때
4. 캐릭터/스타일 LoRA 2~3개를 조합해 쓰고 싶을 때
5. 메타데이터·재현용으로 "어떤 LoRA를 썼는지" 문자열로 남기고 싶을 때
6. 워크플로우 JSON을 사람이 편집할 때 LoRA만 텍스트로 바꾸고 싶을 때
7. 배치에서 프롬프트+LoRA를 한 필드로 넘기고 파싱을 노드에 맡기고 싶을 때
8. 모델 강도와 CLIP 강도를 다르게 주고 싶을 때 (`이름:model_str:clip_str`)
9. 동일 워크플로우로 스타일만 바꿔 여러 결과를 만들고 싶을 때
10. Save Image LM 등과 함께 LoRA 정보를 메타데이터로 저장하고 싶을 때

---

## Lora Stacker
- 입력: lora_stack(LORA_STACK). 출력: LORA_STACK
- 위젯: [lora_name, model_strength, clip_strength] 배열

**사용 상황**
1. LoRA 목록을 배열로 관리하고 Lora Loader (LoraManager)에 넘기고 싶을 때
2. 조건/분기 결과에 따라 다른 LoRA 세트를 스택으로 넘기고 싶을 때
3. 여러 Lora Stacker를 이어 붙여 LoRA 순서·강도를 단계별로 쌓고 싶을 때
4. UI/스크립트에서 [이름, 모델강도, CLIP강도]만 동적으로 만들고 싶을 때
5. Lora Loader의 lora_stack 입력에 기존 스택을 이어 붙이고 싶을 때

---

## RgthreePowerLoraLoader
- 입력: model(MODEL), clip(CLIP). 출력: MODEL, CLIP
- 위젯: lora_name, strength_model(0.5~1.0), strength_clip(1.0 등)

**사용 상황**
1. LoRA를 하나만 쓰고 모델/CLIP 강도를 각각 제어하고 싶을 때
2. 스타일 LoRA는 모델 강도만 높이고 CLIP은 1.0으로 유지하고 싶을 때
3. Lora Loader (LoraManager) 대신 단일 LoRA를 파일명으로 지정하고 싶을 때
4. rgthree 컨텍스트(RgthreeContext)와 함께 쓰는 파이프라인에서 LoRA 하나만 넣고 싶을 때
5. 실험적으로 strength_model / strength_clip을 따로 스윕하고 싶을 때
6. 트리거 워드가 필요 없고 LoRA 적용만 하고 싶을 때
7. 워크플로우에서 LoRA 노드를 한두 개만 쓰고 단순하게 유지하고 싶을 때
8. A/B 테스트로 같은 LoRA에 strength만 바꿔 비교하고 싶을 때
