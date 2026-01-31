# 노드 패턴·참고

## 로딩
- CheckpointLoaderSimple: ckpt_name 정확. Easy Checkpoint Loader: ckpt_hint 부분 일치.
- LoRA: Lora Loader (LoraManager) text `"<lora:이름:강도>"`. 2~3개 이내, 강도 0.5~1.0.

## 이미지 체인
- 기본: Generate → VAEDecode → Save
- 후처리: VAEDecode → easy hiresFix → ColorMatch → Save
- 디테일: VAEDecode → FaceDetailerPipe → EditDetailerPipe(눈/손) → Save
- 전체: VAEDecode → hiresFix → FaceDetailerPipe → ColorMatch → UltimateSDUpscale → Save

## 디테일링
- 얼굴: FaceDetailerPipe(cycle=1). 얼굴+눈: FaceDetailerPipe → EditDetailerPipe(eyes) → FaceDetailerPipe(cycle=2). denoise 0.3~0.5, bbox_threshold 0.5, cycle 1~3.

## 업스케일
- 빠름: easy hiresFix(1.5x). 고품질: UltimateSDUpscale(2~4x, tile 512, denoise 0.2~0.4). 업스케일 전 디테일링 권장.

## ControlNet
- LoadImage → AIO_Preprocessor(Canny/DWPose/Depth 등) → ControlNetLoader → ControlNetApplyAdvanced. strength 0.7~1.0.

## 마스크 크롭
- Image+Mask → Crop By Mask v5 → 처리 → Restore Crop Box v4 → 최종 IMAGE.

## 컨텍스트
- CheckpointLoader → RgthreeContext → 여러 노드에 CONTEXT 전달. RgthreeContextSwitch로 분기.

## 메타데이터
- Input Parameters → Image Saver. filename에 %date% %model% %steps% %seed% 등. PNG 시 워크플로우 포함 가능.

## 주의
- 노드/모델: SD 1.5 vs SDXL 호환 확인. ControlNet 모델과 베이스 버전 일치. YOLO/SAM 모델 경로 models/.
- 메모리: 디테일러 다수/업스케일 타일/배치 크기 ↑ → VRAM ↑.
