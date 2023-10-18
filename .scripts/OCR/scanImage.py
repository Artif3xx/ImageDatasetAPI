import cv2
import numpy as np
import easyocr
import argparse


def cleanup_text(text):
    # strip out non-ASCII text, so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def ocr(srcImage: np.ndarray, useGpu: bool = True, printProb: float = 0.5, langs=None):
    if langs is None:
        langs = ['en', 'de']
    reader = easyocr.Reader(langs, gpu=useGpu)  # this needs to run only once to load the model into memory
    # load the input image from disk
    # OCR the input image using EasyOCR
    print("[INFO] --> OCR'ing input image...")
    results = reader.readtext(srcImage)
    print("---------------------------------")
    # loop over the results
    for (bbox, text, prob) in results:
        # display the OCR'd text and associated probability
        if prob > printProb:
            print("[INFO] --> {:.4f}: {}".format(prob, text))
            # unpack the bounding box
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            # cleanup the text and draw the box surrounding the text along
            # with the OCR'd text itself
            text = cleanup_text(text)
            cv2.rectangle(srcImage, tl, br, (0, 255, 0), 2)
            cv2.putText(srcImage, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            print("[INFO] --> {:.4f}: {}".format(prob, text))
    # show the output image
    cv2.imshow("Image", srcImage)
    # handle the opened windows according to macOS
    cv2.startWindowThread()
    print(cv2.waitKey(0))
    cv2.destroyAllWindows()
    for i in range(2):
        cv2.waitKey(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="scan a picture with easyOCR")
    parser.add_argument("image", metavar='img', type=str,
                        help="The image to scan for characters")

    args = parser.parse_args()

    try:
        image = cv2.imread(getattr(args, 'image'))
    except cv2.error as e:
        print(e)
    finally:
        ocr(image, printProb=0.4)

