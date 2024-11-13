import requests
from bs4 import BeautifulSoup
import csv
import pdfkit
from pdf2image import convert_from_path
import pytesseract
import os
import argparse
from urllib.parse import urljoin, urlparse

# Function to extract all chapter URLs from the page
def extract_chapter_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    chapter_links = []

    # Find all <dd> with class "col-sm-3"
    for dd in soup.find_all('dd', class_='col-sm-3'):
        a_tag = dd.find('a')
        if a_tag and a_tag.get('href'):
            chapter_links.append(urljoin(page_url, a_tag['href']))

    return chapter_links

# Function to extract the pageselect options and get URLs
def extract_pageselect_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <select> element with name="pageselect"
    select_tag = soup.find('select', {'name': 'pageselect'})
    if not select_tag:
        print("没有找到分页选择元素。")
        return []

    # Extract all option values from the select element
    option_values = [option['value'] for option in select_tag.find_all('option') if 'value' in option.attrs]

    # Step 1: Ensure base URL does not end with a chapter part
    if base_url.endswith('.html'):
        base_url = base_url[:base_url.rfind('/')]  # Remove everything after the last '/'

    page_urls = []
    for value in option_values:
        # Step 2: Remove the common part between base_url and value to avoid repetition
        common_path = base_url.rstrip('/')
        if value.startswith(common_path):
            value = value[len(common_path):]  # Remove the base part from value

        # Step 3: Concatenate base_url and value (ensure no duplication)
        full_url = base_url.rstrip('/') + '/' + value.lstrip('/')

        # Check if URL already ends with .html to avoid duplication
        if not full_url.endswith('.html'):
            full_url = full_url.rstrip('/') + '.html'

        page_urls.append(full_url)

    return page_urls

def save_webpage_as_pdf(url, output_path):
    # 使用 pdfkit 将网页转换为 PDF
    try:
        # pdfkit 需要 wkhtmltopdf 的路径
        # 如果 wkhtmltopdf 安装在默认路径，可以跳过配置
        config = pdfkit.configuration()  # 替换为你的 wkhtmltopdf 路径（如果必要）

        # 转换网页为 PDF
        pdfkit.from_url(url, output_path, configuration=config)

        print(f"PDF 已成功保存到 {output_path}")
    except Exception as e:
        print(f"将网页转换为 PDF 时发生错误: {e}")

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
        ocr_text += f"--- 第 {i + 1} 页 ---\n"
        ocr_text += text
        ocr_text += "\n\n"

    # 将提取的文本写入文件
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(ocr_text)

    print(f"文本已保存到 {output_txt}")

# Function to clean up the title and extract the part before the first '_'
def clean_title(title):
    if title:
        return title.split('_')[0].strip()
    return "无标题"

# Main logic to collect all chapter URLs and save to CSV
def main():
    parser = argparse.ArgumentParser(
        description="博宇书屋小说下载器https://www.boyushu.com/。这个脚本可以下载并转换小说章节为 PDF 和 TXT 文件。您可以处理所有章节，也可以通过提供 URL 来处理单个章节。"
    )

    # The base_url is optional, it can be provided for the directory of chapters
    parser.add_argument('base_url', nargs='?', help="小说目录的 URL。需要 URL 页面底下能显示'xxx-xxx章'")

    # -s option allows you to process a single chapter URL
    parser.add_argument('-s', '--single', action='store', help="处理单个章节 URL，将其转换为 PDF 和 TXT 文件")

    # Parse the command-line arguments
    args = parser.parse_args()

    # If neither base_url nor -s option is provided, show help
    if not (args.base_url or args.single):
        parser.print_help()
        return

    # If -s is provided, process the single URL
    if args.single:
        # Process a single URL provided by the user
        url = args.single
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the title of the page
            title = clean_title(soup.title.string.strip() if soup.title else "无标题")

            # Set up the paths for PDF and TXT files
            pdf_filename = f"{title}.pdf"
            txt_filename = f"{title}.txt"

            # Save webpage as PDF
            save_webpage_as_pdf(url, pdf_filename)

            # Convert PDF to TXT using OCR
            pdf_to_text_with_ocr(pdf_filename, txt_filename)

        except Exception as e:
            print(f"处理 URL {url} 时发生错误: {e}")

    elif args.base_url:
        # If base_url is provided, process all chapters
        all_chapter_urls = []

        # Extract additional chapter links from pageselect dropdown
        page_urls = extract_pageselect_urls(args.base_url)
        for page_url in page_urls:
            print(f"正在提取章节链接: {page_url}")
            chapter_urls = extract_chapter_links(page_url)
            all_chapter_urls.extend(chapter_urls)

        # Save all collected chapter URLs to CSV
        with open('novel_chapters.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['章节 URL'])
            for url in all_chapter_urls:
                writer.writerow([url])

        print(f"所有章节链接已保存到 novel_chapters.csv")

        # Process each chapter URL
        for url in all_chapter_urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Get the title of the page
                title = clean_title(soup.title.string.strip() if soup.title else "无标题")

                # Set up the paths for PDF and TXT files
                pdf_filename = f"{title}.pdf"
                txt_filename = f"{title}.txt"

                # Save webpage as PDF
                save_webpage_as_pdf(url, pdf_filename)

                # Convert PDF to TXT using OCR
                pdf_to_text_with_ocr(pdf_filename, txt_filename)

            except Exception as e:
                print(f"处理 URL {url} 时发生错误: {e}")

if __name__ == "__main__":
    main()
