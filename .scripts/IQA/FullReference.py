import argparse
import numpy as np
import cv2 as cv
from skimage.metrics import structural_similarity as ssim


def meanSquareError(referenceImage: np.ndarray, compareImage: np.ndarray) -> float:
    if referenceImage.shape != compareImage.shape:
        raise ValueError("Images must have the same dimensions")

    squared_diff = (referenceImage - compareImage) ** 2

    mse = np.mean(squared_diff, dtype=np.float64)

    return mse


def peakToSignalNoiseRation(referenceImage: np.ndarray, compareImage: np.ndarray, maxPixelValue: int = 255) -> float:
    if referenceImage.shape != compareImage.shape:
        raise ValueError("Images must have the same dimensions")

    mse = np.mean((referenceImage - compareImage) ** 2, dtype=np.float64)

    if mse == 0:
        return float('inf')
    else:
        return 20 * np.log10(maxPixelValue / np.sqrt(mse))


def structuralSimilarityIndex(referenceImage: np.ndarray, compareImage: np.ndarray, dataRange=255) -> float:
    if referenceImage.shape != compareImage.shape:
        raise ValueError("Images must have the same dimensions")

    if len(referenceImage.shape) != 2 or len(compareImage.shape) != 2:
        raise ValueError("Images must be grayscale")

    return ssim(referenceImage, compareImage, data_range=dataRange)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate the full reference image quality metrics")
    # add image arguments to the parser
    parser.add_argument("compare Image", metavar='comp', type=str,
                        help="The image to compare")
    parser.add_argument("reference Image", metavar='ref', type=str,
                        help="The reference image")

    # add metric arguments to the parser
    parser.add_argument('--mse', action='store_true',
                        help="Calculate the mean square error between the images")
    parser.add_argument('--psnr', action='store_true',
                        help="Calculate the peak to signal noise ratio between the images")
    parser.add_argument('--ssim', action='store_true',
                        help="Calculate the structural similarity index between the images. The images will be "
                             "converted to grayscale.")

    # add optional arguments to the parser
    parser.add_argument("--gray", action='store_true',
                        help="(optional) Convert the images to grayscale.")

    args = parser.parse_args()

    if sum([args.mse, args.psnr, args.ssim]) != 1:
        print("You must choose exactly one metric!")
        exit(1)

    if args.mse:
        try:
            compImg = cv.imread(getattr(args, 'compare Image'), cv.IMREAD_GRAYSCALE if args.gray else cv.IMREAD_COLOR)
            refImg = cv.imread(getattr(args, 'reference Image'), cv.IMREAD_GRAYSCALE if args.gray else cv.IMREAD_COLOR)
            print(meanSquareError(refImg, compImg))
        except cv.error as e:
            print(e)
    elif args.psnr:
        try:
            compImg = cv.imread(getattr(args, 'compare Image'), cv.IMREAD_GRAYSCALE if args.gray else cv.IMREAD_COLOR)
            refImg = cv.imread(getattr(args, 'reference Image'), cv.IMREAD_GRAYSCALE if args.gray else cv.IMREAD_COLOR)
            print(peakToSignalNoiseRation(refImg, compImg))
        except cv.error as e:
            print(e)
    elif args.ssim:
        try:
            compImg = cv.imread(getattr(args, 'compare Image'), cv.IMREAD_GRAYSCALE)
            refImg = cv.imread(getattr(args, 'reference Image'), cv.IMREAD_GRAYSCALE)
            print(structuralSimilarityIndex(refImg, compImg), None)
        except cv.error as e:
            print(e)
    else:
        parser.print_help()
