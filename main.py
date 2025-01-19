from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
import os

# Create the FastAPI app instance
app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 1: Add root endpoint for testing
@app.get("/")
async def read_root():
    return {"message": "Welcome to Goodmatch API!"}

# Endpoint to generate a PDF
@app.post("/generate-pdf/")
async def generate_pdf(
    full_name: str = Form(...),
    date_of_birth: str = Form(...),
    place_of_birth: str = Form(...),
    height: str = Form(...),
    education: str = Form(...),
    job_occupation: str = Form(...),
    organization: str = Form(...),
    annual_income: str = Form(...),
    fathers_name: str = Form(...),
    fathers_occupation: str = Form(...),
    mothers_name: str = Form(...),
    mothers_occupation: str = Form(...),
):
    # Path to the HTML template file
    template_path = os.path.join(os.path.dirname(__file__), "html_templates", "biodata_template.html")

    try:
        # Read the HTML template
        with open(template_path, "r", encoding="utf-8") as file:
            biodata_html = file.read()

        # Replace placeholders with form data
        biodata_html = biodata_html.replace("{{full_name}}", full_name)
        biodata_html = biodata_html.replace("{{date_of_birth}}", date_of_birth)
        biodata_html = biodata_html.replace("{{place_of_birth}}", place_of_birth)
        biodata_html = biodata_html.replace("{{height}}", height)
        biodata_html = biodata_html.replace("{{education}}", education)
        biodata_html = biodata_html.replace("{{job_occupation}}", job_occupation)
        biodata_html = biodata_html.replace("{{organization}}", organization)
        biodata_html = biodata_html.replace("{{annual_income}}", annual_income)
        biodata_html = biodata_html.replace("{{fathers_name}}", fathers_name)
        biodata_html = biodata_html.replace("{{fathers_occupation}}", fathers_occupation)
        biodata_html = biodata_html.replace("{{mothers_name}}", mothers_name)
        biodata_html = biodata_html.replace("{{mothers_occupation}}", mothers_occupation)

        # Generate PDF from HTML
        pdf_buffer = BytesIO()
        HTML(string=biodata_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        # Return the PDF as a response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={full_name}_biodata.pdf"}
        )
    except Exception as e:
        return {"error": f"An error occurred while generating the PDF: {str(e)}"}
