# 마스크·크롭 (ComfyUI_Swwan, comfyui-kjnodes)

## Crop By Mask v5
- 입력: image(IMAGE), mask(MASK), padding(INT), force_resize_width/height(INT)
- 출력: IMAGE, crop_box(CROP_BOX), width, height. widgets_values: `[32, 512, 512]`
- 패턴: Image+Mask → Crop By Mask v5 → 처리 → Restore Crop Box v4

## Restore Crop Box v4
- 입력: original_image(IMAGE), cropped_image(IMAGE), crop_box(CROP_BOX), blend_amount(FLOAT)
- 출력: IMAGE. blend_amount 0~1

## CreateGradientMask
- 입력: width, height(INT), start_x, start_y, end_x, end_y(FLOAT 0~1). 출력: MASK

## CreateShapeMask
- 입력: width, height(INT), shape(COMBO circle/square/triangle), x_pos, y_pos, size(FLOAT 0~1). 출력: MASK

## CreateTextMask
- 입력: width, height(INT), text(STRING), font_size(INT), x_pos, y_pos(FLOAT). 출력: MASK

## GrowMaskWithBlur
- 입력: mask(MASK), expand(INT), incremental_expand(BOOL), tapered_corners(BOOL), blur_radius(FLOAT), lerp_alpha(FLOAT). 출력: MASK

## BatchCropFromMaskAdvanced
- 입력: image(IMAGE), mask(MASK), bbox_smooth_alpha(FLOAT), crop_size_mult(FLOAT), bbox_fill(COMBO). 출력: IMAGE(배치), bbox, index
