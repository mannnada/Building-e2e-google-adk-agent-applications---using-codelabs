"""FastAPI server for the Advanced Tool Agent."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from app.agent import AdvancedToolAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Advanced Tool Agent API",
    description="AI agent that generates and analyzes code using Gemini CLI",
    version="1.0.0"
)

agent = AdvancedToolAgent()


class GenerateRequest(BaseModel):
    task: str
    language: str = "python"
    complexity: str = "medium"


class AnalyzeRequest(BaseModel):
    code: str
    analysis_type: str = "security"


class AgentRequest(BaseModel):
    request: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Advanced Tool Agent",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate")
async def generate_code(request: GenerateRequest):
    """Generate code using Gemini CLI."""
    try:
        from app.tools import generate_code_with_cli
        result = generate_code_with_cli(
            task=request.task,
            language=request.language,
            complexity=request.complexity
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_code(request: AnalyzeRequest):
    """Analyze code using Gemini CLI."""
    try:
        from app.tools import analyze_code_with_cli
        result = analyze_code_with_cli(
            code=request.code,
            analysis_type=request.analysis_type
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent")
async def process_agent_request(request: AgentRequest):
    """Process a natural language request through the agent."""
    try:
        result = agent.process_request(request.request)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    except Exception as e:
        logger.error(f"Agent request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
