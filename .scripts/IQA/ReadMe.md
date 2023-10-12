# IAQ - Image Quality Assessment

Is the process of quantifying and comparing the quality of based on certain criteria or metrics. There are two main 
types of IQA:

1. Subjective IQA - involves human observers who rate or rank the images based on their perception and preferences.
2. Objective IQA - involves mathematical models or algorithms that measure or predict the image quality based on some 
features or parameters. This type of IQA is useful for evaluating the technical quality of images.

## 1. Objective IQA

1. Full-Reference IQA (FR-IQA) - compares the reference image with the distorted image. The reference image is the
original image and the distorted image is the image that has been processed or distorted in some way. The difference
between the two images is measured using a metric or algorithm.

   - mean square error (MSE)
   - peak-to-signal noise ratio (PSNR)
   - structural similarity index (SSIM)

2. Reduced-Reference IQA (RR-IQA) - compares the reference image with a reduced set of features extracted from the
reference image. From there on we can evaluate how well the image preserves or degrades the features based on criteria.

   - structural similarity index (SSIM)
   - feature similarity index (FSIM)
   - visual information fidelity (VIF)
   - visual signal-to-noise ratio (VSNR)

3. No-Reference IQA (NR-IQA) - evaluates the quality of an image without any reference image or features.

   - blind image quality index (BIQI)
   - natural image quality evaluator (NIQE)
   - visual information fidelity (VIF)
   - visual signal-to-noise ratio (VSNR)

## 2. Subjective IQA

coming soon ...

*reference: [LinkedIn](https://www.linkedin.com/advice/0/how-do-you-measure-image-quality-machine-vision?locale=en#)*
