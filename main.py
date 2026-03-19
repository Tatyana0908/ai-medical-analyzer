from fastapi import FastAPI, HTTPException
from schemas import LabRequest, LabResponse
from llm import analyze_lab

app = FastAPI(title="AI Medical Analyzer")


@app.post("/analyze", response_model=LabResponse)
def analyze(request: LabRequest):
    try:
        result = analyze_lab(
            data={
                "test_name": request.test_name,
                "values": request.values
            },
            temperature=request.temperature
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
