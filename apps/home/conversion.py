import cv2
import numpy as np
import os
from pdf2image import convert_from_path
from django.conf import settings 


def convert_pdf_to_images(pdf_path, dpi=800):
    images = convert_from_path(pdf_path, dpi, poppler_path=r'C:\Users\Solar\Downloads\poppler-23.01.0\Library\bin')

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('page'+ str(i) +'.bmp', 'bmp')
    return len(images)


def process_image(image_path, uploaded_file):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    real_x, real_y, real_w, real_h = (0, 0, 0, 0)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)

            if x != 0 and real_w * real_h < w * h:
                real_x, real_y, real_w, real_h = x, y, w, h

    crop_img = img[real_y:real_y + real_h, real_x:real_x + real_w]
    img = cv2.bilateralFilter(src=crop_img, d=9, sigmaColor=75, sigmaSpace=75)

    width, height = uploaded_file.width, uploaded_file.height
    dim = (width, height)
    new_image = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    img = cv2.bilateralFilter(src=new_image, d=9, sigmaColor=75, sigmaSpace=75)

    pixel_values = img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)

    k = uploaded_file.color
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)

    new_image = centers[labels.flatten()]
    new_image = new_image.reshape(img.shape)

    return new_image


def main(uploaded_file):
    pdf_path = uploaded_file.file.path
    result = uploaded_file.image_name
    output_image_path = os.path.join(settings.CORE_DIR, 'media', 'converted_files', result)
    
    uploaded_file.image = f'converted_files/{result}'
    uploaded_file.save()
    num_images = convert_pdf_to_images(pdf_path)

    for i in range(num_images):
        image_path = f'page{i}.bmp'
        processed_image = process_image(image_path, uploaded_file)
        cv2.imwrite(output_image_path, processed_image)
        # cv2.imshow(f'Processed Image {i}', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()