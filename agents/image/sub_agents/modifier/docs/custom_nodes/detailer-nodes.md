# 디테일러 (comfyui-impact-pack, comfyui-impact-subpack)

## SAMLoader
- 출력: SAM_MODEL. 위젯 model_name, device_mode. 예: `["sam_vit_b_01ec64.pth", "AUTO"]`

## UltralyticsDetectorProvider
- 출력: BBOX_DETECTOR, SEGM_DETECTOR. 위젯 model_name
- 옵션: bbox/face_yolov8m.pt(얼굴), bbox/eyes_yolov8n.pt(눈), bbox/hand_yolov8n.pt(손), bbox/body_yolov8m.pt(신체), segm/person_yolov8m-seg.pt(사람)

## ToDetailerPipe
- 입력: model, clip, vae, positive, negative, bbox_detector, sam_model_opt, segm_detector_opt
- 출력: detailer_pipe(DETAILER_PIPE) → FaceDetailerPipe/EditDetailerPipe에 전달

## FaceDetailerPipe
- 입력: image(IMAGE), detailer_pipe(DETAILER_PIPE), guide_size(512), max_size(1024), seed, steps, cfg, sampler_name, scheduler, denoise(0.3~0.5), feather, noise_mask, force_inpaint, bbox_threshold(0.5), bbox_dilation, bbox_crop_factor(3.0), sam_*, drop_size, cycle(1~3)
- 출력: IMAGE, cropped_refined, mask, detailer_pipe

## EditDetailerPipe
- 입력: detailer_pipe(DETAILER_PIPE), bbox_detector(BBOX_DETECTOR). 출력: detailer_pipe(DETAILER_PIPE)
- 패턴: Face Detector→ToDetailerPipe→FaceDetailerPipe(얼굴); Eyes/Hand Detector→EditDetailerPipe→FaceDetailerPipe(눈/손)
