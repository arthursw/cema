from pathlib import Path

model = None


def segment(
    input_image: Path | str,
    segmentation: Path | str,
    model_type="cyto",
    use_gpu=False,
    channels=[0, 0],
    auto_diameter=True,
    diameter=30,
):
    global model

    input_image = Path(input_image)
    if not input_image.exists():
        raise Exception(f"Error: input image {input_image} does not exist.")

    print(f"[[1/4]] Load libraries and model {model_type}")
    print("Loading libraries...")
    import cellpose.models
    import cellpose.io

    if model is None or model.cp.model_type != model_type:
        print("Loading model...")
        model = cellpose.models.Cellpose(
            gpu=True if use_gpu == "True" else False, model_type=model_type
        )

    print(f"[[2/4]] Load image {input_image}")
    image = cellpose.io.imread(str(input_image))

    print("[[3/4]] Compute segmentation", image.shape)
    try:
        masks, flows, styles, diams = model.eval(
            image, diameter=None if auto_diameter else int(diameter), channels=channels
        )
    except Exception as e:
        print(e)
        raise e
    print("segmentation finished.")

    segmentation = Path(segmentation)
    print(f"[[4/4]] Save segmentation {segmentation}")
    # save results as png
    cellpose.io.save_masks(image, masks, flows, str(input_image), png=True)
    output_mask = input_image.parent / f"{input_image.stem}_cp_masks.png"
    if output_mask.exists():
        if segmentation.exists():
            segmentation.unlink()
        (output_mask).rename(segmentation)
        print(f"Saved out: {segmentation}")
    else:
        print("Segmentation was not generated because no masks were found.")
    return diams
