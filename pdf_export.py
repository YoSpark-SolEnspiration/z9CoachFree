# File: pdf_export.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_report(profile_data: dict, filename: str = "Z9_Insight_Report.pdf") -> bytes:
    """
    Generate a PDF report for the user profile.

    Args:
        profile_data: Dict containing traits, charts, narratives.
        filename: Output PDF filename (unused, for signature compatibility).

    Returns:
        Bytes of the generated PDF.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 50, "Z9 Insight Engine Report")

    # Summary section
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(50, y, f"Composite Trait Score: {profile_data['trait_score']}")
    y -= 20
    c.drawString(50, y, f"Harmony Ratio: {profile_data['harmony_ratio']}%")
    y -= 20
    c.drawString(50, y, f"Z9 Spiral Stage: {profile_data['stage']}")
    y -= 40

    # Placeholder for chart images (user to embed externally)
    c.drawString(50, y, "[Charts and detailed narratives omitted for brevity]")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()