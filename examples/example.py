from cema.environment_manager import EnvironmentManager
import requests

# Initialize the environment manager
# Cema will use the existing Micromamba installation at the specified path (e.g., "micromamba/") if available;
# otherwise it will automatically download and install Micromamba in a self-contained manner.
environmentManager = EnvironmentManager("micromamba/")

# Create and launch an isolated Conda environment named "cellpose"
env = environmentManager.create("cellpose", {"conda": ["cellpose==3.1.0"]})
env.launch()

# Download example image from cellpose
imagePath = "cellpose_img02.png"
imageData = requests.get("https://www.cellpose.org/static/images/img02.png").content
with open(imagePath, "wb") as handler:
    handler.write(imageData)

segmentationPath = imagePath.replace(".png", "_segmentation.png")

# Import example_module in the environment
example_module = env.importModule("example_module.py")
# example_module is a proxy to example_module.py in the environment,
# calling example_module.function_name(args) will run env.execute(module_name, function_name, args)
diameters = example_module.segment(imagePath, segmentationPath)

# Or use env.execute() directly
# diameters = env.execute("example_module.py", "segment", (imagePath, segmentationPath))

print(f"Found diameters of {diameters} pixels.")

# Clean up and exit the environment
env.exit()
