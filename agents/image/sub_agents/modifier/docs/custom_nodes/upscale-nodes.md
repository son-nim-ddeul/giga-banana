# 업스케일

**패키지:** comfyui_ultimatesdupscale, comfyui-easy-use  
→ [CUSTOM_NODE_SUMMARY](../CUSTOM_NODE_SUMMARY.md) | [WORKFLOW_CREATION_GUIDE](../WORKFLOW_CREATION_GUIDE.md) | [patterns-best-practices](patterns-best-practices.md)

---

## UltimateSDUpscale
- 입력: image, model, positive, negative, vae, upscale_model(선택), upscale_by(2~4), seed, steps, cfg, sampler_name, scheduler, denoise(0.2~0.4), mode_type(Linear/Chess/None), tile_width/height(512), seam_fix_*, force_uniform_tiles, tiled_decode
- 출력: IMAGE. seam_fix_mode Band Pass 권장

**사용 상황**
1. 1024×1024를 2048×2048 이상으로 고품질 업스케일하고 싶을 때
2. VRAM이 적어도 타일 단위로 나눠 큰 이미지를 처리하고 싶을 때
3. tile 512로 타일 크기를 맞춰 품질/속도 균형을 잡고 싶을 때
4. denoise 0.2~0.4로 원본을 유지하면서 디테일만 보강하고 싶을 때
5. seam_fix_mode Band Pass로 타일 경계를 부드럽게 하고 싶을 때
6. mode_type Linear/Chess로 타일 순서를 바꿔 아티팩트를 줄이고 싶을 때
7. 2x, 4x 등 upscale_by로 목표 배율을 지정하고 싶을 때
8. 디테일러(얼굴/손) 적용 후 최종 업스케일로 출력하고 싶을 때
9. 포스터/인쇄용 고해상도 출력이 필요할 때
10. easy hiresFix보다 품질을 우선하고 시간/VRAM을 허용할 때

---

## easy hiresFix
- 입력: image, model, positive, negative, vae, upscale_by(1.5~2), steps(10~20), denoise(0.3~0.5)
- 출력: IMAGE. widgets_values 예: `[1.5, 15, 0.4]`

**사용 상황**
1. 빠르게 1.5x~2x 해상도를 올리고 싶을 때
2. UltimateSDUpscale보다 단순한 한 노드로 해상도 향상하고 싶을 때
3. 메모리/시간이 제한적일 때 가벼운 업스케일이 필요할 때
4. 미리보기/초안용으로 빠른 업스케일이 필요할 때
5. 512/768 결과를 1024 정도로만 올리고 싶을 때
6. denoise를 낮게 해 원본 구도를 유지하고 싶을 때
7. steps 10~20으로 짧게 돌려 속도를 우선하고 싶을 때
8. 파이프라인에서 "간단 업스케일" 단계 하나만 넣고 싶을 때
9. UltimateSDUpscale 전에 1.5x로 먼저 올리고 싶을 때
10. 배치/자동화에서 가벼운 업스케일만 필요할 때
