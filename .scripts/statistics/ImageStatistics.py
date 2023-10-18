from __future__ import annotations

import numpy as np
import cv2 as cv


class ImageStatistics:
    statistics: dict = None

    def __init__(self, file: str | np.ndarray):
        if isinstance(file, str):
            self.filepath = file
            self.image_rgb = self.read()
        else:
            self.image_rgb = file
        self.image_gray = cv.cvtColor(self.image_rgb, cv.COLOR_RGB2GRAY)

    def read(self):
        img = cv.imread(self.filepath, cv.IMREAD_COLOR)
        return cv.cvtColor(img, cv.COLOR_BGR2RGB)

    def get_statistics(self):
        self.collect_statistics()
        return self.statistics

    def collect_statistics(self):
        brightness_rgb = np.average(np.linalg.norm(self.image_rgb, axis=2)) / np.sqrt(3)
        brightness_gray = np.average(self.image_gray)

        # Berechne das Signal (durchschnittliche Helligkeit des Bildes)
        signal = np.mean(self.image_gray)

        # Berechne das Rauschen (Standardabweichung der Helligkeit des Bildes)
        noise = np.std(self.image_gray)

        # Berechne das Signal-Rausch-Verhältnis (SNR)
        snr = signal / noise

        # Berechne die Schärfe des Bildes (z.B. mit Laplacian-Methode)
        sharpness = cv.Laplacian(self.image_gray, cv.CV_64F).var()

        self.statistics = {
            "brightness_rgb": {"score": brightness_rgb, "method": "Euclidean norm"},
            "brightness_gray": {"score": brightness_gray, "method": "Average"},
            "noise": {"score": noise, "method": "Standard Deviation"},
            "signal2noise": {"score": snr, "method": "Signal to Noise Ratio"},
            "sharpness": {"score": sharpness, "method": "Laplacian"}
        }

    def get_image(self):
        return cv.cvtColor(self.image_rgb, cv.COLOR_RGB2BGR)

    @staticmethod
    def write_values_on_image(image, values_dict):
        # Erstelle eine Kopie des Bildes, um das Original nicht zu verändern
        result_image = image.copy()
        width = image.shape[1] / 650
        print(width)

        # Schriftart und Schriftgröße für die Legende
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = int(width) if int(width) > 0 else 1
        font_color = (255, 255, 255)  # Weiß
        font_thickness = 2 * font_scale

        # Position für die Legende (links oben im Bild)
        x, y = 20 * int(width), 40 * int(width)

        # Schreibe die Werte aus dem Dictionary in die Legende
        for key, value in values_dict.items():
            legend_text = f"{key}: {value['score']:.2f}"
            cv.putText(result_image, legend_text, (x, y), font, font_scale, font_color, font_thickness)
            y += 40 * int(width)  # Versatz für den nächsten Eintrag

        return result_image

