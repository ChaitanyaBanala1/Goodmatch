from fastapi import FastAPI, Request
from weasyprint import HTML
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the FastAPI app instance
app = FastAPI()

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a specific domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

# Endpoint to generate a PDF
@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    try:
        form_data = await request.json()
    except Exception as e:
        return {"error": f"Invalid JSON payload: {str(e)}"}

    # Extract fields from the form data
    full_name = form_data.get("full_name", "N/A")
    date_of_birth = form_data.get("date_of_birth", "N/A")
    place_of_birth = form_data.get("place_of_birth", "N/A")
    height = form_data.get("height", "N/A")
    education = form_data.get("education", "N/A")
    job_occupation = form_data.get("job_occupation", "N/A")
    organization = form_data.get("organization", "N/A")
    annual_income = form_data.get("annual_income", "N/A")
    fathers_name = form_data.get("fathers_name", "N/A")
    fathers_occupation = form_data.get("fathers_occupation", "N/A")
    mothers_name = form_data.get("mothers_name", "N/A")
    mothers_occupation = form_data.get("mothers_occupation", "N/A")

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
