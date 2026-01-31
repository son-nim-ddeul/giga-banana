# 노드 패턴·참고

→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md)

---

## 로딩
- CheckpointLoaderSimple: ckpt_name 정확. Easy Checkpoint Loader: ckpt_hint 부분 일치.
- LoRA: Lora Loader (LoraManager) text `"<lora:이름:강도>"`. 2~3개 이내, 강도 0.5~1.0.

**이 패턴을 쓰는 상황**
1. 파일명을 정확히 알고 있을 때 → CheckpointLoaderSimple
2. 파일명이 길거나 여러 버전이 있을 때 → Easy Checkpoint Loader(힌트)
3. 프롬프트와 LoRA를 한 문자열로 관리하고 싶을 때 → Lora Loader (LoraManager)
4. 외부 API/설정에서 LoRA 정보를 텍스트로 받을 때
5. 재현용으로 "어떤 LoRA를 썼는지" 문자열로 남기고 싶을 때
6. 2~3개 LoRA를 조합해 스타일/캐릭터를 만들 때
7. 트리거 워드를 자동 추출해 프롬프트에 붙이고 싶을 때
8. A/B 테스트로 체크포인트/LoRA만 바꿔 비교할 때
9. 배치/자동화에서 모델 선택을 힌트/텍스트로만 하고 싶을 때
10. 팀/프로젝트에서 설정을 JSON·텍스트로 공유할 때

---

## 이미지 체인
- 기본: Generate → VAEDecode → Save
- 후처리: VAEDecode → easy hiresFix → ColorMatch → Save
- 디테일: VAEDecode → FaceDetailerPipe → EditDetailerPipe(눈/손) → Save
- 전체: VAEDecode → hiresFix → FaceDetailerPipe → ColorMatch → UltimateSDUpscale → Save

**이 패턴을 쓰는 상황**
1. 텍스트→이미지만 필요할 때 → 기본 체인
2. 해상도를 빠르게 올리고 싶을 때 → hiresFix
3. 참조 이미지 색감을 맞추고 싶을 때 → ColorMatch
4. 인물/일러스트 얼굴·손 품질을 올리고 싶을 때 → FaceDetailerPipe + EditDetailerPipe
5. 최종 출력을 고해상도로 내고 싶을 때 → UltimateSDUpscale
6. 시리즈/에피소드 색조 통일이 필요할 때 → ColorMatch
7. 업스케일 전에 얼굴/손을 먼저 보정하고 싶을 때 → 디테일 → 업스케일
8. 한 번에 "해상도↑ + 디테일↑ + 색보정 + 저장"을 하고 싶을 때 → 전체 체인
9. VRAM/시간에 따라 hiresFix vs UltimateSDUpscale 중 선택할 때
10. 배치 결과마다 동일 후처리 파이프를 적용할 때

---

## 디테일링
- 얼굴: FaceDetailerPipe(cycle=1). 얼굴+눈: FaceDetailerPipe → EditDetailerPipe(eyes) → FaceDetailerPipe(cycle=2). denoise 0.3~0.5, bbox_threshold 0.5, cycle 1~3.

**이 패턴을 쓰는 상황**
1. 생성 결과 얼굴이 흐리거나 왜곡되었을 때
2. 인물 사진/일러스트 품질을 올리고 싶을 때
3. 눈/손 아티팩트만 따로 보정하고 싶을 때 (EditDetailerPipe)
4. 업스케일 전에 얼굴/손을 먼저 보정하고 싶을 때
5. 여러 인물이 있는 장면에서 각각 얼굴을 보정하고 싶을 때
6. cycle 1~3으로 보정 강도를 조절하고 싶을 때
7. denoise를 낮게 해 원본을 유지하면서 디테일만 보강하고 싶을 때
8. 5단계 디테일링(얼굴→눈→얼굴→손→얼굴)을 하고 싶을 때
9. ToDetailerPipe로 파이프를 한 번 만들고 감지기만 바꿔 쓰고 싶을 때
10. SAM + YOLO 조합으로 정교한 마스크가 필요할 때

---

## 업스케일
- 빠름: easy hiresFix(1.5x). 고품질: UltimateSDUpscale(2~4x, tile 512, denoise 0.2~0.4). 업스케일 전 디테일링 권장.

**이 패턴을 쓰는 상황**
1. 빠르게 1.5~2x만 올리고 싶을 때 → hiresFix
2. 2x~4x 고품질 업스케일이 필요할 때 → UltimateSDUpscale
3. VRAM이 적을 때 타일 크기(512 등)로 조절하고 싶을 때
4. 포스터/인쇄용 고해상도가 필요할 때
5. 디테일러 적용 후 최종 업스케일로 출력하고 싶을 때
6. denoise를 낮게 해 원본 구도를 유지하고 싶을 때
7. seam_fix로 타일 경계를 부드럽게 하고 싶을 때
8. 시간/VRAM에 따라 hiresFix vs UltimateSDUpscale 중 선택할 때
9. 배치 결과를 동일 업스케일 설정으로 저장할 때
10. 실험적으로 배율·denoise·타일을 바꿔 최적값을 찾을 때

---

## ControlNet
- LoadImage → AIO_Preprocessor(Canny/DWPose/Depth 등) → ControlNetLoader → ControlNetApplyAdvanced. strength 0.7~1.0.

**이 패턴을 쓰는 상황**
1. 참조 이미지의 구도(엣지)를 유지하고 싶을 때 → Canny
2. 참조 이미지의 인물 포즈를 유지하고 싶을 때 → DWPose
3. 참조 이미지의 깊이/레이아웃을 유지하고 싶을 때 → Depth
4. 선화/스케치를 참조해 채색하고 싶을 때 → LineArt
5. 한 노드에서 전처리기만 바꿔 Canny/Depth/Pose를 전환하고 싶을 때
6. strength 0.7~1.0으로 제어 강도를 조절하고 싶을 때
7. 여러 ControlNet을 순차 적용하고 싶을 때
8. img2img/포즈 변형/스타일 이전이 필요할 때
9. 동일 구도에 프롬프트만 바꿔 여러 결과를 만들고 싶을 때
10. 베이스 모델과 ControlNet 모델 버전을 맞추고 싶을 때

---

## 마스크 크롭
- Image+Mask → Crop By Mask v5 → 처리 → Restore Crop Box v4 → 최종 IMAGE.

**이 패턴을 쓰는 상황**
1. 특정 영역(얼굴, 손, 객체)만 잘라 후처리하고 원본에 복원하고 싶을 때
2. VRAM을 아끼기 위해 큰 이미지 중 일부만 처리하고 싶을 때
3. 배경은 유지하고 객체만 수정하고 싶을 때
4. SAM/세그멘트 마스크로 영역을 잘라 디테일러/업스케일하고 싶을 때
5. 여러 객체를 BatchCropFromMaskAdvanced로 크롭해 각각 처리하고 싶을 때
6. padding/crop_box로 경계 블렌딩을 조절하고 싶을 때
7. 인페인팅/리터칭 전에 대상 영역만 크롭하고 싶을 때
8. CreateShapeMask/CreateGradientMask 등으로 마스크를 만들고 크롭하고 싶을 때
9. GrowMaskWithBlur로 마스크 경계를 부드럽게 한 뒤 크롭하고 싶을 때
10. 동일 위치에 Restore Crop Box로 합쳐 최종 이미지를 만들고 싶을 때

---

## 컨텍스트
- CheckpointLoader → RgthreeContext → 여러 노드에 CONTEXT 전달. RgthreeContextSwitch로 분기.

**이 패턴을 쓰는 상황**
1. 연결선을 줄여 워크플로우를 정리하고 싶을 때
2. 여러 노드에 같은 MODEL/CLIP/VAE/프롬프트를 한 줄로 주고 싶을 때
3. 모델/설정을 조건에 따라 바꾸고 싶을 때 (RgthreeContextSwitch)
4. 디테일러/업스케일 파이프에서 "설정 묶음"을 재사용하고 싶을 때
5. A/B 테스트로 서로 다른 CONTEXT를 전환하고 싶을 때
6. 시드만 바꾼 여러 샘플러에 동일 CONTEXT를 넘기고 싶을 때
7. 워크플로우 가독성/유지보수를 높이고 싶을 때
8. 4개까지 설정을 미리 만들어 스위치로 선택하고 싶을 때
9. CONTEXT를 저장/불러와 설정을 재사용하고 싶을 때
10. "한 곳만 바꾸면 전체 파이프라인 설정이 바뀌는" 구조를 만들고 싶을 때

---

## 메타데이터
- Input Parameters → Image Saver. filename에 %date% %model% %steps% %seed% 등. PNG 시 워크플로우 포함 가능.

**이 패턴을 쓰는 상황**
1. 재현용으로 생성 파라미터를 파일명/메타데이터에 남기고 싶을 때
2. 나중에 동일 설정으로 재실행하고 싶을 때
3. A/B 테스트 결과를 설정별로 구분해 저장하고 싶을 때
4. LoRA 정보를 메타데이터에 포함하고 싶을 때 (Save Image LM)
5. %date%, %time%, %counter%로 파일/폴더를 자동 정리하고 싶을 때
6. 외부 툴에서 메타데이터만 읽어 재현/추가 처리하고 싶을 때
7. PNG에 ComfyUI 워크플로우+A1111 스타일 메타데이터를 넣고 싶을 때
8. 실험 로그/버전 관리에서 설정을 추적하고 싶을 때
9. 배치 저장 시 파일명이 겹치지 않게 플레이스홀더로 구분하고 싶을 때
10. 팀/프로젝트에서 "어떤 설정으로 만들었는지" 공유하고 싶을 때

---

## 주의
- 노드/모델: SD 1.5 vs SDXL 호환 확인. ControlNet 모델과 베이스 버전 일치. YOLO/SAM 모델 경로 models/.
- 메모리: 디테일러 다수/업스케일 타일/배치 크기 ↑ → VRAM ↑.
