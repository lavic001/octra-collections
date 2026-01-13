from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# --- CONFIGURATION ---
TEMPLATE_FILE = 'template.pdf'
OUTPUT_FILE = 'Template_With_Grid.pdf'

def create_grid_overlay(width, height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    # Settings for the grid
    can.setFont("Helvetica", 8)
    can.setStrokeColorRGB(0.7, 0.7, 0.7)  # Light Grey
    can.setLineWidth(0.5)

    # DRAW VERTICAL LINES (X Axis)
    # Step = 50 points
    for x in range(0, int(width), 50):
        can.line(x, 0, x, height)
        can.drawString(x + 2, 10, str(x)) # Label at bottom
        can.drawString(x + 2, height - 20, str(x)) # Label at top

    # DRAW HORIZONTAL LINES (Y Axis)
    # Step = 20 points (More frequent because vertical spacing is tight)
    for y in range(0, int(height), 20):
        can.line(0, y, width, y)
        can.drawString(5, y + 2, str(y)) # Label at left
        can.drawString(width - 25, y + 2, str(y)) # Label at right

    can.save()
    packet.seek(0)
    return packet

def main():
    print(f"Generating grid for {TEMPLATE_FILE}...")
    
    # 1. Read the template to get size
    try:
        reader = PdfReader(TEMPLATE_FILE)
        page = reader.pages[0]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
    except FileNotFoundError:
        print(f"Error: Could not find '{TEMPLATE_FILE}'")
        return

    # 2. Create the Grid
    grid_packet = create_grid_overlay(width, height)
    grid_pdf = PdfReader(grid_packet)

    # 3. Merge
    writer = PdfWriter()
    page.merge_page(grid_pdf.pages[0])
    writer.add_page(page)

    # 4. Save
    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)
    
    print(f"✅ DONE! Open '{OUTPUT_FILE}' to see your coordinates.")

if __name__ == "__main__":
    main()
