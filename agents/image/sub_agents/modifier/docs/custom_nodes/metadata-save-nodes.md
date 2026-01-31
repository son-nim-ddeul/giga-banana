# 메타데이터·저장 (comfyui-image-saver, comfyui-lora-manager, ComfyUI-EasyFilePaths)

## Image Saver
- 입력: images(IMAGE), filename(STRING), path(STRING), extension(STRING), steps, cfg, modelname, sampler_name, scheduler, positive, negative, seed_value, width, height, lossless_webp, quality_jpeg_or_webp, counter, time_format
- 파일명 플레이스홀더: %date%, %time%, %model%, %steps%, %cfg%, %seed%, %counter%, %width%, %height%. 예: `output_%date%_%time%_%model%_s%steps%_seed%seed%_%counter%`

## Input Parameters (Image Saver)
- 입력: steps, cfg, sampler_name, scheduler, denoise, seed(INT). 출력: METADATA → Image Saver 등에 연결

## Save Image LM
- 입력: images(IMAGE), filename(STRING), lora_info(STRING). LoRA 정보 메타데이터 포함 저장

## Easy JSON Job Tracker
- 입력: job_file(STRING), mode(COMBO). 출력: job_data, job_id. mode: get_next, mark_done, add_job
