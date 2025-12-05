import cv2


class ScanErrors:
    def __init__(self, min_area=30):
        self.min_area = min_area

    def classify(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area < self.min_area:
            return None

        aspect_ratio = max(w, h) / max(1, min(w, h))

        if aspect_ratio > 3.5:
            return "CRACK", (0, 255, 255)  # Yellow
        elif aspect_ratio < 2.5:
            return "POROSITY", (0, 0, 255)  # Red
        return None

    def scan_and_draw(self, img_gray, edges_closed):
        contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        count_crack = 0
        count_porosity = 0

        # 1. Vẽ các khung lỗi
        for cnt in contours:
            result = self.classify(cnt)
            if result is None:
                continue

            label, color = result
            x, y, w, h = cv2.boundingRect(cnt)

            if label == "CRACK":
                count_crack += 1
            else:
                count_porosity += 1

            pad = 3
            cv2.rectangle(img_out, (x - pad, y - pad), (x + w + pad, y + h + pad), color, 2)
            cv2.putText(img_out, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # 2. VẼ LABEL THỐNG KÊ GÓC TRÁI TRÊN (HUD)
        # ---------------------------------------------------------
        total_errors = count_crack + count_porosity

        # Tạo khung nền đen mờ ở góc trái để chữ dễ đọc hơn
        # Tọa độ (x1, y1) là (10, 10), (x2, y2) tùy chỉnh theo độ dài chữ
        overlay = img_out.copy()
        cv2.rectangle(overlay, (5, 5), (200, 95), (0, 0, 0), -1)
        alpha = 0.6  # Độ trong suốt của nền đen
        cv2.addWeighted(overlay, alpha, img_out, 1 - alpha, 0, img_out)

        # Vẽ viền trắng cho khung thông tin
        cv2.rectangle(img_out, (5, 5), (200, 95), (255, 255, 255), 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 1
        line_height = 25
        start_x = 15
        start_y = 30

        # Dòng 1: Tổng số lỗi (Màu trắng)
        cv2.putText(img_out, f"Total Errors: {total_errors}",
                    (start_x, start_y), font, font_scale, (255, 255, 255), thickness)

        # Dòng 2: Crack (Màu Vàng - theo màu định nghĩa ở trên)
        cv2.putText(img_out, f"- Crack: {count_crack}",
                    (start_x, start_y + line_height), font, font_scale, (0, 255, 255), thickness)

        # Dòng 3: Porosity (Màu Đỏ - theo màu định nghĩa ở trên)
        cv2.putText(img_out, f"- Porosity: {count_porosity}",
                    (start_x, start_y + line_height * 2), font, font_scale, (0, 0, 255), thickness)
        # ---------------------------------------------------------

        return img_out, count_crack, count_porosity
"""
    def scan_and_draw(self, img_gray, edges_closed):
        contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        count_crack = 0
        count_porosity = 0

        for cnt in contours:
            result = self.classify(cnt)
            if result is None:
                continue

            label, color = result
            x, y, w, h = cv2.boundingRect(cnt)

            if label == "CRACK":
                count_crack += 1
            else:
                count_porosity += 1

            pad = 3
            cv2.rectangle(img_out, (x - pad, y - pad), (x + w + pad, y + h + pad), color, 2)
            cv2.putText(img_out, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        return img_out, count_crack, count_porosity
    
"""


