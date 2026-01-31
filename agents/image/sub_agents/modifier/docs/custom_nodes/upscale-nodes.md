# 업스케일 (comfyui_ultimatesdupscale, comfyui-easy-use)

## UltimateSDUpscale
- 입력: image, model, positive, negative, vae, upscale_model(선택), upscale_by(2~4), seed, steps, cfg, sampler_name, scheduler, denoise(0.2~0.4), mode_type(Linear/Chess/None), tile_width/height(512), seam_fix_*, force_uniform_tiles, tiled_decode
- 출력: IMAGE. seam_fix_mode Band Pass 권장

## easy hiresFix
- 입력: image, model, positive, negative, vae, upscale_by(1.5~2), steps(10~20), denoise(0.3~0.5)
- 출력: IMAGE. widgets_values 예: `[1.5, 15, 0.4]`
