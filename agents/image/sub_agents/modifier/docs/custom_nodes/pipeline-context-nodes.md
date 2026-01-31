# 파이프라인·컨텍스트 (rgthree-comfy, comfyui-easy-use)

## RgthreeContext / RgthreeContextBig
- 입력: model, clip, vae, positive, negative, latent, images, seed. 출력: CONTEXT(RGTHREE_CONTEXT) + MODEL, CLIP, VAE, POSITIVE, NEGATIVE, LATENT, IMAGE, SEED
- 하위 노드는 CONTEXT 한 줄만 받아 사용. RgthreeContextSwitch와 조건부 분기

## RgthreeContextSwitch
- 입력: ctx_01, ctx_02, ctx_03, ctx_04(RGTHREE_CONTEXT). 출력: CONTEXT. 위젯으로 인덱스 선택(1→ctx_02)

## easy fullLoader
- 위젯: ckpt_name, config_name, vae_name, clip_skip(-2), lora_name, lora_model_strength, lora_clip_strength, resolution(1024x1024), empty_latent_width/height, positive, negative, batch_size
- 출력: PIPE_LINE, MODEL, VAE, CLIP, CONDITIONING(positive), CONDITIONING(negative), LATENT
