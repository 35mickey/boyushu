import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# 设置 Tesseract 可执行文件路径（如果需要，视你的操作系统而定）
# Windows 用户可能需要修改为自己的安装路径
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_text_with_ocr(pdf_path, output_txt):
    # 将 PDF 转换为图像
    images = convert_from_path(pdf_path)

    # 存储 OCR 结果
    ocr_text = ''

    # 遍历每一页图像
    for i, image in enumerate(images):
        # 转为灰度图像
        image = image.convert('L')
        # 使用 pytesseract 从图像中提取简体中文文本
        text = pytesseract.image_to_string(image, lang='chi_sim')
        ocr_text += f"--- Page {i + 1} ---\n"
        ocr_text += text
        ocr_text += "\n\n"

    # 将提取的文本写入文件
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(ocr_text)

    print(f"Text has been saved to {output_txt}")

if __name__ == "__main__":
    # 输入 PDF 文件路径和输出 TXT 文件路径
    pdf_file = input("Enter the PDF file path: ")
    txt_file = input("Enter the output TXT file path: ")

    pdf_to_text_with_ocr(pdf_file, txt_file)
