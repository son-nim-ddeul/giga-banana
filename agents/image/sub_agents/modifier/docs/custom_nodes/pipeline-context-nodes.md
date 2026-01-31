# 파이프라인·컨텍스트

**패키지:** rgthree-comfy, comfyui-easy-use  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## RgthreeContext / RgthreeContextBig
- 입력: model, clip, vae, positive, negative, latent, images, seed. 출력: CONTEXT(RGTHREE_CONTEXT) + MODEL, CLIP, VAE, POSITIVE, NEGATIVE, LATENT, IMAGE, SEED
- 하위 노드는 CONTEXT 한 줄만 받아 사용. RgthreeContextSwitch와 조건부 분기

**사용 상황**
1. CheckpointLoader 등에서 나온 MODEL/CLIP/VAE/프롬프트를 한 덩어리로 넘기고 싶을 때
2. 연결선을 줄여 워크플로우를 정리하고 싶을 때
3. 여러 노드(KSampler, hiresFix, Detailer 등)에 같은 설정을 CONTEXT 한 줄로 주고 싶을 때
4. RgthreeContextSwitch로 모델/설정을 조건에 따라 바꾸고 싶을 때
5. 분기 후 여러 경로가 같은 CONTEXT를 공유하고 싶을 때
6. 시드만 바꾼 여러 샘플러에 동일 CONTEXT를 넘기고 싶을 때
7. 디테일러/업스케일 파이프에서 "모델·프롬프트 묶음"을 재사용하고 싶을 때
8. 워크플로우 가독성을 높이고 싶을 때
9. CONTEXT를 저장/불러와 설정을 재사용하고 싶을 때
10. 여러 체크포인트/프롬프트 조합을 CONTEXT로 만들어 전환하고 싶을 때

---

## RgthreeContextSwitch
- 입력: ctx_01, ctx_02, ctx_03, ctx_04(RGTHREE_CONTEXT). 출력: CONTEXT. 위젯으로 인덱스 선택(1→ctx_02)

**사용 상황**
1. 두 가지 이상의 모델/설정 중 하나를 선택해 다음 노드에 넘기고 싶을 때
2. RgthreeContext를 여러 개 만들어 스위치로 전환하고 싶을 때
3. A/B 테스트로 서로 다른 체크포인트·프롬프트를 인덱스로 선택하고 싶을 때
4. 조건(시드, 배치 인덱스 등)에 따라 CONTEXT를 바꾸고 싶을 때
5. 한 KSampler/디테일러에 "경로별로 다른 CONTEXT"를 주고 싶을 때
6. 4개까지 설정을 미리 만들어 두고 위젯으로 골라 쓰고 싶을 때
7. 워크플로우에서 "모델 전환"만 스위치 하나로 하고 싶을 때
8. 실험용으로 여러 설정을 한 번에 준비해 두고 번갈아 실행하고 싶을 때
9. ImpactSwitch와 달리 CONTEXT 전체를 바꾸고 싶을 때
10. UI에서 0,1,2,3만 바꿔 전체 파이프라인 설정을 전환하고 싶을 때

---

## easy fullLoader
- 위젯: ckpt_name, config_name, vae_name, clip_skip(-2), lora_name, lora_model_strength, lora_clip_strength, resolution(1024x1024), empty_latent_width/height, positive, negative, batch_size
- 출력: PIPE_LINE, MODEL, VAE, CLIP, CONDITIONING(positive), CONDITIONING(negative), LATENT

**사용 상황**
1. 체크포인트·VAE·LoRA·해상도·프롬프트를 한 노드에서 설정하고 싶을 때
2. 빠른 프로토타이핑/테스트용으로 최소 연결로 파이프라인을 만들고 싶을 때
3. 초보자가 "한 곳만 수정하면 되는" 올인원 로더를 쓰고 싶을 때
4. resolution으로 1024x1024 등 고정 해상도를 쓰고 싶을 때
5. clip_skip -2 등 모델별 설정을 한 노드에 모으고 싶을 때
6. LoRA 하나 + 강도를 한 노드에서 지정하고 싶을 때
7. EmptyLatentImage 대신 empty_latent_width/height로 latent를 받고 싶을 때
8. positive/negative를 위젯으로 넣어 CLIPTextEncode 없이 CONDITIONING을 받고 싶을 때
9. batch_size를 올려 한 번에 여러 장 생성하고 싶을 때
10. 워크플로우를 짧게 유지하면서 기본 txt2img 파이프라인을 만들고 싶을 때
