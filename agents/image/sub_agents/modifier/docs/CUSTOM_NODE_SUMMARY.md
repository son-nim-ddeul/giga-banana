# 커스텀 노드 요약

상세: [custom_nodes/](custom_nodes/) — file-path-loaders, lora-nodes, image-nodes, mask-crop-nodes, detailer-nodes, upscale-nodes, controlnet-nodes, pipeline-context-nodes, utility-nodes, metadata-save-nodes, patterns-best-practices

## 패키지 (↔ 상세 문서)

| 패키지 | 기능 | 상세 문서 |
|--------|------|------------|
| ComfyUI-EasyFilePaths | 파일 경로·힌트 로더·JSON 작업 추적 | [file-path-loaders](custom_nodes/file-path-loaders.md), [metadata-save-nodes](custom_nodes/metadata-save-nodes.md) |
| ComfyUI_Swwan | 마스크 크롭/복원, 리사이즈 | [mask-crop-nodes](custom_nodes/mask-crop-nodes.md), [image-nodes](custom_nodes/image-nodes.md) |
| comfyui-custom-scripts | 수식 계산, 워크플로우 관리 | [utility-nodes](custom_nodes/utility-nodes.md) |
| comfyui-easy-use | 올인원 로더, XY Plot, 프롬프트 처리 | [image-nodes](custom_nodes/image-nodes.md), [upscale-nodes](custom_nodes/upscale-nodes.md), [pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md) |
| comfyui-image-saver | 메타데이터 포함 이미지 저장 | [metadata-save-nodes](custom_nodes/metadata-save-nodes.md) |
| comfyui-impact-pack | 디테일러, SAM, 와일드카드 | [detailer-nodes](custom_nodes/detailer-nodes.md), [utility-nodes](custom_nodes/utility-nodes.md) |
| comfyui-impact-subpack | Ultralytics YOLO 감지기 | [detailer-nodes](custom_nodes/detailer-nodes.md) |
| comfyui-kjnodes | 마스크, 이미지 유틸, 배치 | [image-nodes](custom_nodes/image-nodes.md), [mask-crop-nodes](custom_nodes/mask-crop-nodes.md), [utility-nodes](custom_nodes/utility-nodes.md) |
| comfyui-lora-manager | LoRA 관리, 트리거 워드 | [lora-nodes](custom_nodes/lora-nodes.md), [metadata-save-nodes](custom_nodes/metadata-save-nodes.md) |
| comfyui_controlnet_aux | ControlNet 전처리기 (40개+) | [controlnet-nodes](custom_nodes/controlnet-nodes.md) |
| comfyui_ultimatesdupscale | 타일 업스케일 | [upscale-nodes](custom_nodes/upscale-nodes.md) |
| rgthree-comfy | 컨텍스트, 파워 프롬프트, 시드 | [lora-nodes](custom_nodes/lora-nodes.md), [image-nodes](custom_nodes/image-nodes.md), [pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md), [utility-nodes](custom_nodes/utility-nodes.md) |

## 노드별 타입·기능

### 파일·로더 ([file-path-loaders](custom_nodes/file-path-loaders.md), [lora-nodes](custom_nodes/lora-nodes.md))
| 노드 | 패키지 | 출력 | 비고 |
|------|--------|------|------|
| Easy Checkpoint Loader | ComfyUI-EasyFilePaths | MODEL, CLIP, VAE | widgets: ckpt_hint |
| Easy LoRA Loader | ComfyUI-EasyFilePaths | MODEL | lora_hint, strength_model |
| Easy VAE Loader | ComfyUI-EasyFilePaths | VAE | vae_hint |
| Character LoRA Select | ComfyUI-EasyFilePaths | lora_*, power_*, character_prompt | configs/character_config.json |
| Easy File Name | ComfyUI-EasyFilePaths | relative_path, absolute_path, user | story_path, user_name |
| Lora Loader (LoraManager) | comfyui-lora-manager | MODEL, CLIP, trigger_words | text: `<lora:이름:강도>` |
| Lora Stacker | comfyui-lora-manager | LORA_STACK | [name, model_str, clip_str] |
| RgthreePowerLoraLoader | rgthree-comfy | MODEL, CLIP | lora_name, strength_model/clip |

### 이미지 ([image-nodes](custom_nodes/image-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| ImageResizeKJ | comfyui-kjnodes | IMAGE→IMAGE | width, height, divisible_by |
| Image Scale By Aspect Ratio v2 | ComfyUI_Swwan | IMAGE→IMAGE | aspect_ratio "16:9" |
| ImageBatchMulti | comfyui-kjnodes | IMAGE×n→IMAGE | 배치 결합 |
| GetImagesFromBatchIndexed | comfyui-kjnodes | IMAGE, indexes→IMAGE | "0,2,4" |
| ColorMatch | comfyui-kjnodes | image, reference→IMAGE | method: mkl, hm, reinhard |
| easy imageColorMatch | comfyui-easy-use | image, reference→IMAGE | 색상 매칭 |
| ImageGridComposite3x3 | comfyui-kjnodes | image1~9→IMAGE | 3×3 그리드 |
| RgthreeImageComparer | rgthree-comfy | image_a, image_b | UI 비교용(출력 없음) |

### 마스크·크롭 ([mask-crop-nodes](custom_nodes/mask-crop-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| Crop By Mask v5 | ComfyUI_Swwan | IMAGE,MASK→IMAGE,crop_box | padding, force_resize |
| Restore Crop Box v4 | ComfyUI_Swwan | original_image,cropped_image,crop_box→IMAGE | |
| CreateGradientMask, CreateShapeMask, CreateTextMask | comfyui-kjnodes | →MASK | |
| GrowMaskWithBlur | comfyui-kjnodes | MASK→MASK | |
| BatchCropFromMaskAdvanced | comfyui-kjnodes | IMAGE,MASK→IMAGE | |

### 디테일러 ([detailer-nodes](custom_nodes/detailer-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| SAMLoader | comfyui-impact-pack | →SAM_MODEL | sam_vit_b_01ec64.pth |
| UltralyticsDetectorProvider | comfyui-impact-subpack | →BBOX_DETECTOR,SEGM_DETECTOR | face/eyes/hand/body_yolo |
| ToDetailerPipe | comfyui-impact-pack | model,clip,vae,pos,neg,bbox,sam,segm→DETAILER_PIPE | |
| FaceDetailerPipe | comfyui-impact-pack | image,detailer_pipe→IMAGE | guide_size 512, denoise 0.3~0.5, cycle 1~3 |
| EditDetailerPipe | comfyui-impact-pack | detailer_pipe+다른 감지기→IMAGE | 눈/손 등 |

### 업스케일 ([upscale-nodes](custom_nodes/upscale-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| UltimateSDUpscale | comfyui_ultimatesdupscale | image,model,pos,neg,vae,upscale_model→IMAGE | upscale_by 2~4, denoise 0.2~0.4, tile 512 |
| easy hiresFix | comfyui-easy-use | image,model,pos,neg,vae→IMAGE | upscale_by 1.5~2, steps 10~20 |

### ControlNet ([controlnet-nodes](custom_nodes/controlnet-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| AIO_Preprocessor | comfyui_controlnet_aux | preprocessor,image,resolution→IMAGE | Canny/HED/LineArt/Depth/DWPose 등 |
| ControlNetLoader | (기본) | →CONTROL_NET | |
| ControlNetApplyAdvanced | (기본) | positive,negative,control_net,image→CONDITIONING | |

### 파이프라인·컨텍스트 ([pipeline-context-nodes](custom_nodes/pipeline-context-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| RgthreeContext / RgthreeContextBig | rgthree-comfy | MODEL,CLIP,VAE,pos,neg,…→CONTEXT+개별 | |
| RgthreeContextSwitch | rgthree-comfy | ctx_01~04→CONTEXT | 인덱스 선택 |
| easy fullLoader | comfyui-easy-use | 위젯→PIPE_LINE,MODEL,VAE,CLIP,CONDITIONING×2,LATENT | ckpt,vae,clip_skip,lora,해상도,프롬프트 |

### 유틸 ([utility-nodes](custom_nodes/utility-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| MathExpression\|pysssss | comfyui-custom-scripts | a,b,c→INT/FLOAT | "a*b+c" |
| SimpleCalculatorKJ | comfyui-kjnodes | a,b,operation→result | add/subtract/multiply/divide |
| RgthreeSeed / Seed (rgthree) | rgthree-comfy | →INT | −1=랜덤 |
| ImpactSwitch | comfyui-impact-pack | select,input1~4→selected | |
| ImpactWildcardProcessor | comfyui-impact-pack | text→STRING | {A\|B\|C} 랜덤 치환 |
| Reroute | (기본 등) | *→* | 패스스루 |
| RgthreePowerPrompt | rgthree-comfy | 프롬프트 강화 | |
| StringConcatenate | (다수) | 문자열,구분자→STRING | |

### 저장·메타데이터 ([metadata-save-nodes](custom_nodes/metadata-save-nodes.md))
| 노드 | 패키지 | 입출력 | 비고 |
|------|--------|--------|------|
| Image Saver | comfyui-image-saver | images,filename,path,… | 플레이스홀더 %date% %model% %seed% |
| Input Parameters (Image Saver) | comfyui-image-saver | steps,cfg,sampler,…→METADATA | |
| Save Image LM | comfyui-lora-manager | images,filename,lora_info | |
| Easy JSON Job Tracker | ComfyUI-EasyFilePaths | job_file,mode→job_data,job_id | get_next/mark_done/add_job |

## 용도별 노드 매핑 ([patterns-best-practices](custom_nodes/patterns-best-practices.md))

- 모델/로드: Easy Checkpoint/LoRA/VAE Loader, easy fullLoader
- LoRA 여러 개: Lora Loader (LoraManager), Lora Stacker
- 크기/비율: ImageResizeKJ, Image Scale By Aspect Ratio v2
- 색 보정: ColorMatch, easy imageColorMatch
- 영역만 처리: Crop By Mask v5 → 처리 → Restore Crop Box v4
- 얼굴/눈/손: FaceDetailerPipe + EditDetailerPipe + UltralyticsDetectorProvider
- 업스케일: UltimateSDUpscale(타일), easy hiresFix(간단)
- 포즈/엣지/깊이: ControlNet + AIO_Preprocessor(DWPose/Canny/Depth 등)
- 재현용 저장: Image Saver + Input Parameters + Save Image LM
