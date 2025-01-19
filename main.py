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

template_path = os.path.join(os.path.dirname(__file__), "html_templates", "biodata_template.html")
if not os.path.exists(template_path):
    raise FileNotFoundError("HTML template file not found. Please ensure it exists in the correct path.")


@app.get("/")
def root():
    return {"message": "Welcome to the Goodmatch API!"}

@app.get("/generate-pdf/")
def pdf_instructions():
    return {
        "message": "This endpoint only supports POST requests. Please submit a valid form with JSON payload."
    }

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

        # Validate required fields
        required_fields = ["full_name"]
        missing_fields = [key for key in required_fields if key not in fields]
        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

        # Read and process the HTML template
        template_path = os.path.join(os.path.dirname(__file__), "html_templates", "biodata_template.html")
        if not os.path.exists(template_path):
            return {"error": "HTML template file not found."}

        with open(template_path, "r", encoding="utf-8") as file:
            biodata_html = file.read()

         # Replace placeholders
        for key, value in fields.items():
            placeholder = f"{{{{{key.replace('-', '_').lower()}}}}}"  # Convert "Full-Name" to "{{full_name}}"
            biodata_html = biodata_html.replace(placeholder, value or "N/A")

        logging.info(f"Processed HTML: {biodata_html}")

        # Generate PDF
        pdf_buffer = BytesIO()
        HTML(string=biodata_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

       # Set the filename
        filename = fields.get("full_name", "biodata").replace(" ", "_") + ".pdf"

        # Return the PDF
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={fields.get('full_name', 'biodata')}.pdf"}
        )
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return {"error": "The HTML template file is missing. Please contact support."}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}
