# ComfyUI 워크플로우 작성 가이드 (에이전트 참고용)

Workflow JSON **Version 0.4** 기준. 노드 ID·링크 ID 고유, 타입 일치, 순환 참조 금지.

## JSON 구조

**최상위:** `id`, `revision`, `last_node_id`, `last_link_id`, `nodes`, `links`, `groups`, `config`, `extra`, `version: 0.4`

**노드:** `id`, `type`, `pos`, `size`, `order`, `mode` (0=활성, 4=비활성), `inputs`, `outputs`, `widgets_values`

**링크:** `[link_id, source_node_id, source_slot, target_node_id, target_slot, type]` (슬롯 0부터)

## 데이터 타입

| 타입 | 사용처 |
|------|--------|
| MODEL | Checkpoint → LoRA → KSampler |
| CLIP | Checkpoint → CLIPTextEncode |
| VAE | Checkpoint/VAELoader → VAEDecode |
| CONDITIONING | CLIPTextEncode → KSampler |
| LATENT | EmptyLatentImage/VAEEncode → KSampler → VAEDecode |
| IMAGE | VAEDecode → 후처리 → Image Saver |
| MASK | Detailer, Crop By Mask |
| DETAILER_PIPE | ToDetailerPipe → FaceDetailerPipe/EditDetailerPipe |
| BBOX_DETECTOR, SAM_MODEL | UltralyticsDetectorProvider, SAMLoader → ToDetailerPipe |
| CONTROL_NET | ControlNetLoader → ControlNetApplyAdvanced |
| UPSCALE_MODEL | UpscaleModelLoader → UltimateSDUpscale |
| COMBO | sampler_name, scheduler 등 |

## 노드 생성 순서 (의존성)

1. **로드:** CheckpointLoaderSimple → (VAELoader) → (CLIPSetLastLayer) → (Lora Loader) → …
2. **프롬프트:** (ImpactWildcardProcessor) → CLIPTextEncode(+) → CLIPTextEncode(-)
3. **생성:** EmptyLatentImage 또는 LoadImage+VAEEncode → (Seed) → KSampler
4. **디코딩:** (ImpactSwitch) → VAEDecode
5. **후처리(선택):** easy hiresFix, easy imageColorMatch, UltimateSDUpscale, ControlNet, FaceDetailerPipe/EditDetailerPipe
6. **저장:** (Input Parameters) → Image Saver

## 필수 노드 입출력

- **CheckpointLoaderSimple:** 출력 MODEL, CLIP, VAE. 위젯 `ckpt_name`.
- **CLIPTextEncode:** 입력 clip(CLIP), text(STRING). 출력 CONDITIONING.
- **EmptyLatentImage:** 출력 LATENT. 위젯 width, height, batch_size.
- **KSampler:** 입력 model, positive, negative, latent_image, seed, steps, cfg, sampler_name, scheduler, denoise. 출력 LATENT. sampler 예: dpmpp_2m_sde_gpu. scheduler 예: karras.
- **VAEDecode:** 입력 samples(LATENT), vae(VAE). 출력 IMAGE.
- **Image Saver:** 입력 images(IMAGE), filename, path, extension 등.

## 규칙

- 노드/링크 ID: 고유, 신규 추가 시 last_node_id/last_link_id 증가 후 사용.
- 링크: 출력 타입과 입력 타입 일치. source/target 노드 ID 존재해야 함.
- 순환 참조 금지 (DAG 유지).
- 필수 노드는 mode 0. 끄려면 mode 4 (구조만 유지).

## 파일 경로

- 체크포인트: `models/checkpoints/`
- LoRA: `models/loras/`
- VAE: `models/vae/`
- ControlNet: `models/controlnet/`
- 업스케일: `models/upscale_models/`
- 출력: `output/` 등

## 최소 텍스트→이미지 연결

```
CheckpointLoaderSimple ─ MODEL → KSampler
                         CLIP → CLIPTextEncode(+) ─ CONDITIONING → KSampler
                         CLIP → CLIPTextEncode(-) ─ CONDITIONING → KSampler
                         VAE  → VAEDecode
EmptyLatentImage ─ LATENT → KSampler ─ LATENT → VAEDecode ─ IMAGE → Image Saver
```

## 선택 노드 요약

- **LoRA:** Lora Loader (LoraManager) text `"<lora:이름:강도>"` → MODEL/CLIP.
- **CLIP Skip:** CLIPSetLastLayer stop_at_clip_layer -1 또는 -2.
- **디테일러:** SAMLoader + UltralyticsDetectorProvider → ToDetailerPipe → FaceDetailerPipe/EditDetailerPipe. guide_size 512, denoise 0.3~0.5, cycle 1~3.
- **업스케일:** easy hiresFix(1.5~2x) 또는 UltimateSDUpscale(2~4x, tile 512, denoise 0.2~0.4).
- **ControlNet:** LoadImage → AIO_Preprocessor(Canny/DWPose/Depth 등) → ControlNetLoader → ControlNetApplyAdvanced → CONDITIONING에 병합.

## 이미지·샘플링 권장

- 해상도: 512~1024 (빠름), 1024~2048 (균형). steps 20~30, cfg 7~12. 디테일러 cycle 1~3, 업스케일 denoise 낮게.
