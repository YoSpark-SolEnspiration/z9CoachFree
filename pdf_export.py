# ✅ File: pdf_export.py — for FREE app only

import pdfkit

def generate_simple_report(data):
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 30px; }}
            h1 {{ color: #4B0082; }}
            p {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>Z9 Coach Free — Insight Report</h1>
        <p><strong>Composite Trait Score:</strong> {data['trait_score']:.2f}</p>
        <p><strong>Harmony Ratio:</strong> {data['harmony_ratio']:.2f}%</p>
        <p><strong>Stage:</strong> {data['stage']}</p>
        <h2>Your Trait Summary</h2>
        <p>{data['trait_summary']}</p>
        <p>Thank you for using Z9 Coach Free. For full visuals & coaching, upgrade to Lite or Pro.</p>
    </body>
    </html>
    """
    pdf_bytes = pdfkit.from_string(html, False)
    return pdf_bytes
