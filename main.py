from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from weasyprint import HTML
from io import BytesIO
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://goodmatch.webflow.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-pdf/")
async def generate_pdf(
    full_name: str = Form(..., alias="fields[First%20Name]"),
    date_of_birth: str = Form(..., alias="fields[Date%20of%20Birth]"),
    place_of_birth: str = Form(..., alias="fields[Place%20of%20Birth]"),
    height: str = Form(..., alias="fields[Height]"),
    education: str = Form(..., alias="fields[Education]"),
    job_occupation: str = Form(..., alias="fields[Job%20%2F%20Occupation]"),
    organization: str = Form(..., alias="fields[Organization]"),
    annual_income: str = Form(..., alias="fields[Annual%20Income]"),
    fathers_name: str = Form(..., alias="fields[Father's%20Name]"),
    fathers_occupation: str = Form(..., alias="fields[Father's%20Occupation]"),
    mothers_name: str = Form(..., alias="fields[Mother's%20Name]"),
    mothers_occupation: str = Form(..., alias="fields[Mother's%20Occupation]"),
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

        # Generate PDF
        pdf_buffer = BytesIO()
        HTML(string=biodata_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={full_name}_biodata.pdf"},
        )
    except Exception as e:
        return {"error": f"An error occurred while generating the PDF: {str(e)}"}
