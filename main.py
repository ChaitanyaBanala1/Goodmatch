from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create the FastAPI app instance
app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Goodmatch API!"}

@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    try:
        # Parse the incoming payload
        try:
            form_data = await request.json()
        except Exception as e:
            logging.error(f"Invalid JSON payload: {e}")
            return {"error": f"Invalid JSON payload: {str(e)}"}

        logging.info(f"Received payload: {form_data}")

        # Check if the 'fields' key exists in the payload
        fields = form_data.get("fields")
        if not fields:
            return {"error": "Missing 'fields' in the payload."}

        # Read and process the HTML template
        template_path = os.path.join(os.path.dirname(__file__), "html_templates", "biodata_template.html")
        if not os.path.exists(template_path):
            return {"error": "HTML template file not found."}

        with open(template_path, "r", encoding="utf-8") as file:
            biodata_html = file.read()

        # Replace placeholders dynamically
        for key, value in fields.items():
            placeholder = f"{{{{{key}}}}}"  # Convert "Full Name" to "{{Full Name}}"
            biodata_html = biodata_html.replace(placeholder, value or "N/A")

        # Generate PDF
        pdf_buffer = BytesIO()
        HTML(string=biodata_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        # Return the PDF
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={fields.get('Full Name', 'biodata')}.pdf"}
        )
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        return {"error": f"An error occurred while generating the PDF: {str(e)}"}
