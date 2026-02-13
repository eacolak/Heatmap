import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Heatmap.src.utils.response import build_response
from components.Heatmap.src.models.PackageModel import PackageModel


class HeatmapExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.image = self.request.get_param("inputImage")
        self.detections = self.request.get_param("inputDetections")

        self.do_filter_idle_detections = self.request.get_param("FilterIdleDetections")
        if self.do_filter_idle_detections:
            self.iou_threshold = self.request.get_param("MovementIouThreshold")
        else:
            self.iou_threshold = 0.95  # this wont be used but still

        self.radius_coeff = self.request.get_param("RadiusCoefficient")
        self.colormap_key = self.request.get_param("ColorMap")

        if self.request.get_param("AdvancedConfigs") == "True":
            self.gaussian_blur_kernel_size = self.request.get_param(
                "GaussianBlurKernelSize"
            )
            self.heatmap_alpha = self.request.get_param("HeatmapAlpha")
            self.heatmap_beta = self.request.get_param("HeatmapBeta")
            self.heatmap_gamma = self.request.get_param("HeatmapGamma")
            self.decay_factor = self.request.get_param("DecayFactor")
            self.heat_intensity_divisor = self.request.get_param("HeatIntensityDivisor")
        elif self.request.get_param("AdvancedConfigs") == "False":
            self.gaussian_blur_kernel_size = 35
            self.heatmap_alpha = 0.6
            self.heatmap_beta = 0.4
            self.heatmap_gamma = 0
            self.decay_factor = 0.99
            self.heat_intensity_divisor = 25.0

        self.heatmap_data = self.bootstrap["heatmap_data"]
        self.prev_detections = self.bootstrap["prev_detections"]

    @staticmethod
    def bootstrap(config: dict) -> dict:
        heatmap_data = None
        prev_detections = None

        return {"heatmap_data": heatmap_data, "prev_detections": prev_detections}

    def get_accumulated_heatmap(self, frame_shape: tuple) -> np.ndarray:
        if self.heatmap_data is None or self.heatmap_data.shape[:2] != frame_shape[:2]:
            return np.zeros(frame_shape[:2], dtype=float)
        else:
            return self.heatmap_data

    def save_accumulated_heatmap(self, heatmap_canvas: np.ndarray):
        self.heatmap_data = heatmap_canvas
        self.bootstrap["heatmap_data"] = self.heatmap_data

    def heatmap_effect(self, box: dict, heatmap_canvas: np.ndarray) -> None:
        left = int(box["left"])
        top = int(box["top"])
        width = int(box["width"])
        height = int(box["height"])

        x0, y0 = left, top
        x1, y1 = left + width, top + height

        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(heatmap_canvas.shape[1], x1)
        y1 = min(heatmap_canvas.shape[0], y1)

        if x1 <= x0 or y1 <= y0:
            return

        base_radius = min(width, height) // 2
        radius = int((base_radius * self.radius_coeff) / 100)

        if radius <= 0:
            return

        radius_squared = radius**2

        xv, yv = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))

        center_x = (x0 + x1) // 2
        center_y = (y0 + y1) // 2
        dist_squared = (xv - center_x) ** 2 + (yv - center_y) ** 2

        within_radius = dist_squared <= radius_squared

        pixel_count = np.sum(within_radius)
        if pixel_count > 0:
            # Use a reference area so small/medium boxes behave as before
            reference_area = 500
            # Scale the increment inversely with area (sqrt to soften the effect)
            normalized_increment = 2 * np.sqrt(reference_area / pixel_count)
            heatmap_canvas[y0:y1, x0:x1][within_radius] += normalized_increment

    def calculate_iou(self, box1: dict, box2: dict) -> float:
        x1_min = box1["left"]
        y1_min = box1["top"]
        x1_max = box1["left"] + box1["width"]
        y1_max = box1["top"] + box1["height"]

        x2_min = box2["left"]
        y2_min = box2["top"]
        x2_max = box2["left"] + box2["width"]
        y2_max = box2["top"] + box2["height"]

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        if inter_x_max <= inter_x_min or inter_y_max <= inter_y_min:
            return 0.0

        intersection = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)

        area1 = box1["width"] * box1["height"]
        area2 = box2["width"] * box2["height"]
        union = area1 + area2 - intersection

        if union == 0:
            return 0.0

        return intersection / union

    def filter_idle_detections(self):
        if self.bootstrap["prev_detections"] is None:
            return self.detections

        prev_bboxes = [
            det.get("boundingBox") for det in self.bootstrap["prev_detections"]
        ]

        filtered_detections = []
        for det in self.detections:
            bbox = det.get("boundingBox")
            if bbox is None:
                filtered_detections.append(det)
                continue

            is_new = True
            for prev_bbox in prev_bboxes:
                if prev_bbox is None:
                    continue

                iou = self.calculate_iou(bbox, prev_bbox)
                if iou >= self.iou_threshold:
                    is_new = False
                    break

            if is_new:
                filtered_detections.append(det)

        return filtered_detections

    def generate_heatmap_overlay(self, image: np.ndarray) -> np.ndarray:
        heatmap_canvas = self.get_accumulated_heatmap(image.shape)

        if self.heatmap_data is not None:
            self.heatmap_data *= self.decay_factor

        detections = (
            self.filter_idle_detections()
            if self.do_filter_idle_detections
            else self.detections
        )

        if detections:
            for detection in detections:
                try:
                    bbox = detection["boundingBox"]
                    self.heatmap_effect(bbox, heatmap_canvas)
                except (KeyError, TypeError, ValueError) as e:
                    print(
                        f"Skipping a detection due to unexpected format: {detection}. Error: {e}",
                        file=sys.stderr,
                    )
                    continue

        self.save_accumulated_heatmap(heatmap_canvas)

        viz_heatmap = heatmap_canvas.copy()

        if np.max(viz_heatmap) > 0:
            viz_heatmap = cv2.GaussianBlur(
                viz_heatmap,
                (self.gaussian_blur_kernel_size, self.gaussian_blur_kernel_size),
                0,
            )

        if np.max(viz_heatmap) > 0:
            viz_heatmap = (viz_heatmap / self.heat_intensity_divisor) * 255
            viz_heatmap = np.clip(viz_heatmap, 0, 255)

        viz_heatmap = viz_heatmap.astype(np.uint8)
        heatmap_colored = cv2.applyColorMap(
            viz_heatmap, getattr(cv2, self.colormap_key)
        )

        if len(image.shape) == 2 or image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        if image.dtype != heatmap_colored.dtype:
            image = image.astype(heatmap_colored.dtype)

        superimposed_img = cv2.addWeighted(
            image,
            self.heatmap_alpha,
            heatmap_colored,
            self.heatmap_beta,
            self.heatmap_gamma,
        )

        return superimposed_img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.generate_heatmap_overlay(img.value)

        self.image = Image.set_frame(
            img=img, package_uID=self.uID, redis_db=self.redis_db
        )

        print(f"Heatmap: {self.image}")
        self.data_dict = self.image.dict()
        print(f"Heatmap: {self.data_dict}")

        self.bootstrap["prev_detections"] = self.detections

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
