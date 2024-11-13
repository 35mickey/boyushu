# 博宇书屋小说下载器https://www.boyushu.com/

这个 Python 脚本可以下载并转换小说章节为 PDF 和 TXT 文件，支持批量下载章节，也可以通过指定单个 URL 下载并转换为文件。

## 功能

- 自动提取章节链接
- 将网页保存为 PDF 文件
- 使用 OCR 将 PDF 文件转换为 TXT 文件
- 支持处理所有章节或者单独处理一个章节

## 安装依赖

首先需要安装一些依赖库：

```bash
pip install requests beautifulsoup4 pdfkit pdf2image pytesseract
sudo apt install wkhtmltopdf tesseract-ocr
```

## 使用方法

1. 处理单个章节
使用 -s 选项指定单个章节 URL：

```bash
python3 boyushu.py -s https://www.boyushu.com/qepx6u/wq6ydy1/itahljktn.html
```
这将下载指定的章节并将其转换为 PDF 和 TXT 文件。

2. 处理所有章节
如果你有一个小说目录的 URL，可以处理所有章节：

```bash
python3 boyushu.py https://www.boyushu.com/qepx6u/wq6ydy1/3-1.html
```
这将提取目录页面中的所有章节链接，并将每个章节转换为 PDF 和 TXT 文件。