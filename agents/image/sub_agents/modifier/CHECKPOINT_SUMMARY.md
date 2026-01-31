# 체크포인트 요약

`docs/checkpoints/` 문서를 기반으로 한 체크포인트 모델 요약입니다.  
워크플로 노드에서 사용 시 `widgets_values`에 아래 형식으로 모델 파일명을 지정합니다.

---

## 1. DreamShaper 8

- **widgets_values**: `["dreamshaper_8.safetensors"]`
- **특성**: 일러스트·아트 중심. 다용도 품질은 부가적.
- **권장 설정**
  - CLIP skip 2 사용 가능
  - ENSD: 31337 (재현용, 필수 아님)
  - highres.fix 또는 고해상도 img2img 권장
  - ADetailer 사용 시 얼굴이 비슷해질 수 있음
  - "restore faces" 비권장

---

## 2. v1-5-pruned-ema

- **widgets_values**: `["v1-5-pruned-ema.safetensors"]`
- **특성**: 애니메이션 파스텔 스타일. Hard(강한 파스텔)·Soft(부드러운 파스텔) 버전 존재.
- **권장 설정**
  - CLIP skip 2
  - ENSD: 31337 (선택)
  - "restore faces" 사용 안 함
  - Highres fix: 일반 업스케일러+낮은 denoise 또는 Latent+높은 denoise
  - Baked VAE 버전은 VAE를 Auto로, no VAE 버전은 적절한 VAE 사용. anythingv3 VAE는 회색 톤 유발 가능
  - 스텝·업스케일 denoise는 샘플러·업스케일러에 맞게 조정

---

## widgets_values 사용 예시

체크포인트 로더 노드 등에서 모델 선택 시:

```json
"widgets_values": ["dreamshaper_8.safetensors"]
```

```json
"widgets_values": ["v1-5-pruned-ema.safetensors"]
```

모델 이름만 바꿔서 `"widgets_values": ["{{model name}}.safetensors"]` 형식으로 사용하면 됩니다.
