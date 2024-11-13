import pdfkit

def save_webpage_as_pdf(url, output_path):
    # 使用 pdfkit 将网页转换为 PDF
    try:
        # pdfkit 需要 wkhtmltopdf 的路径
        # 如果 wkhtmltopdf 安装在默认路径，可以跳过配置
        config = pdfkit.configuration()  # 替换为你的 wkhtmltopdf 路径（如果必要）

        # 转换网页为 PDF
        pdfkit.from_url(url, output_path, configuration=config)

        print(f"PDF saved successfully to {output_path}")
    except Exception as e:
        print(f"Error converting webpage to PDF: {e}")

if __name__ == "__main__":
    # 输入网页 URL 和输出 PDF 文件路径
    url = input("Enter the webpage URL: ")
    output_pdf = input("Enter the output PDF file path: ")

    save_webpage_as_pdf(url, output_pdf)
