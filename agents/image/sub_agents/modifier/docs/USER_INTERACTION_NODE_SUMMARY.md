# 유저 상호작용 노드 요약

유저에게 값을 묻거나 선택을 받아야 하는 노드만 정리했습니다.  
상세: [custom_nodes/](custom_nodes/) — file-path-loaders, lora-nodes, image-nodes, mask-crop-nodes, detailer-nodes, upscale-nodes, controlnet-nodes

## 용도

요구사항 구체화 단계에서 **유저가 선택·입력할 수 있는 옵션**을 파악할 때 이 문서와 상세 문서만 참고하세요.  
워크플로우 최적화·내부 구조용 노드(파이프라인 컨텍스트, 유틸, 메타데이터 저장, 패턴)는 image_generator 에이전트가 별도로 참고합니다.

## 패키지 (↔ 상세 문서)

| 패키지 | 유저와 상호작용 포인트 | 상세 문서 |
|--------|------------------------|------------|
| ComfyUI-EasyFilePaths | 체크포인트/LoRA/VAE 힌트, 캐릭터 설정, 파일명·유저명 | [file-path-loaders](custom_nodes/file-path-loaders.md) |
| comfyui-lora-manager | LoRA 선택, 트리거 워드, 강도 | [lora-nodes](custom_nodes/lora-nodes.md) |
| rgthree-comfy | LoRA 선택·강도 | [lora-nodes](custom_nodes/lora-nodes.md) |
| ComfyUI_Swwan, comfyui-kjnodes | 해상도·비율, 색보정, 마스크·크롭 옵션 | [image-nodes](custom_nodes/image-nodes.md), [mask-crop-nodes](custom_nodes/mask-crop-nodes.md) |
| comfyui-impact-pack, comfyui-impact-subpack | 디테일러(얼굴/눈/손) 옵션, 가이드 크기, denoise, cycle | [detailer-nodes](custom_nodes/detailer-nodes.md) |
| comfyui-easy-use, comfyui_ultimatesdupscale | 업스케일 비율, denoise, hiresFix | [upscale-nodes](custom_nodes/upscale-nodes.md) |
| comfyui_controlnet_aux | ControlNet 전처리기 종류, 해상도 | [controlnet-nodes](custom_nodes/controlnet-nodes.md) |

## 노드별 유저 입력·선택 요약

### 파일·로더 ([file-path-loaders](custom_nodes/file-path-loaders.md), [lora-nodes](custom_nodes/lora-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| Easy Checkpoint Loader | ckpt_hint (모델 힌트) |
| Easy LoRA Loader | lora_hint, strength_model |
| Easy VAE Loader | vae_hint |
| Character LoRA Select | config 기반 캐릭터/스타일 선택 |
| Easy File Name | story_path, user_name |
| Lora Loader (LoraManager) | `<lora:이름:강도>` 텍스트 |
| RgthreePowerLoraLoader | lora_name, strength_model/clip |

### 이미지 ([image-nodes](custom_nodes/image-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| ImageResizeKJ | width, height, divisible_by |
| Image Scale By Aspect Ratio v2 | aspect_ratio (예: "16:9") |
| ColorMatch / easy imageColorMatch | 참조 이미지, 메서드 |

### 마스크·크롭 ([mask-crop-nodes](custom_nodes/mask-crop-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| Crop By Mask v5 | padding, force_resize |
| CreateGradientMask, CreateShapeMask, CreateTextMask | 마스크 형태/텍스트 |

### 디테일러 ([detailer-nodes](custom_nodes/detailer-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| FaceDetailerPipe | guide_size, denoise, cycle |
| EditDetailerPipe | 감지기(눈/손 등) 선택 |

### 업스케일 ([upscale-nodes](custom_nodes/upscale-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| UltimateSDUpscale | upscale_by, denoise, tile |
| easy hiresFix | upscale_by, steps |

### ControlNet ([controlnet-nodes](custom_nodes/controlnet-nodes.md))
| 노드 | 유저에게 받을 수 있는 값 |
|------|--------------------------|
| AIO_Preprocessor | preprocessor 종류(Canny/HED/LineArt/Depth/DWPose 등), resolution |

## 상세 문서 목록 (유저 상호작용용)

- [file-path-loaders](custom_nodes/file-path-loaders.md)
- [lora-nodes](custom_nodes/lora-nodes.md)
- [image-nodes](custom_nodes/image-nodes.md)
- [mask-crop-nodes](custom_nodes/mask-crop-nodes.md)
- [detailer-nodes](custom_nodes/detailer-nodes.md)
- [upscale-nodes](custom_nodes/upscale-nodes.md)
- [controlnet-nodes](custom_nodes/controlnet-nodes.md)
