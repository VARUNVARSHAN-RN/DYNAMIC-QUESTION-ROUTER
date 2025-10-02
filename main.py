"""
FastAPI backend for the Dynamic Question Router.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import logging
from contextlib import asynccontextmanager

from classifier import classifier
from chatbots import router
from feedback_storage import storage
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class QuestionRequest(BaseModel):
    """Request model for question input."""
    question: str = Field(..., min_length=1, description="The question to be answered")


class QuestionResponse(BaseModel):
    """Response model for question answering."""
    question: str
    domain: str
    difficulty: str
    confidence: Dict[str, float]
    chatbot_used: str
    answer: str
    success: bool


class FeedbackRequest(BaseModel):
    """Request model for feedback submission."""
    question: str = Field(..., description="The original question")
    predicted_domain: str
    predicted_difficulty: str
    chatbot_used: str
    response: str
    feedback_positive: bool = Field(..., description="True if positive, False if negative")
    corrected_domain: Optional[str] = Field(None, description="Corrected domain if feedback is negative")
    corrected_difficulty: Optional[str] = Field(None, description="Corrected difficulty if feedback is negative")


class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    message: str
    success: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting Dynamic Question Router API...")
    logger.info(f"Classification model: {config.CLASSIFICATION_MODEL}")
    logger.info(f"Available domains: {config.DOMAINS}")
    logger.info(f"Available difficulties: {config.DIFFICULTIES}")
    yield
    # Shutdown
    logger.info("Shutting down Dynamic Question Router API...")


# Initialize FastAPI app
app = FastAPI(
    title="Dynamic Question Router",
    description="Multi-task question classifier with chatbot routing system",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Dynamic Question Router API",
        "version": "1.0.0",
        "endpoints": {
            "/ask": "POST - Submit a question for classification and answering",
            "/feedback": "POST - Submit feedback for a previous answer",
            "/health": "GET - Check API health status",
            "/stats": "GET - Get feedback statistics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "classifier_loaded": True,
        "chatbots_available": list(router.chatbots.keys())
    }


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint: classify question and route to appropriate chatbot.
    
    Workflow:
    1. Classify question domain and difficulty using DeBERTaV3
    2. Apply rule-based routing to select chatbot
    3. Get response from selected chatbot (with fallback)
    4. Return answer to user
    """
    try:
        question = request.question.strip()
        
        # Step 1: Classify the question
        logger.info(f"Classifying question: {question[:50]}...")
        domain, difficulty, confidence = classifier.classify(question)
        
        # Step 2: Apply routing rules
        routing_key = (domain, difficulty)
        chatbot_name = config.ROUTING_RULES.get(routing_key, config.FALLBACK_CHATBOT)
        logger.info(f"Routing to chatbot: {chatbot_name} (Domain: {domain}, Difficulty: {difficulty})")
        
        # Step 3: Get response from chatbot
        answer, actual_chatbot = router.route_question(question, chatbot_name)
        
        if answer is None:
            raise HTTPException(
                status_code=503,
                detail="All chatbot services are unavailable. Please try again later."
            )
        
        # Step 4: Return response
        return QuestionResponse(
            question=question,
            domain=domain,
            difficulty=difficulty,
            confidence=confidence,
            chatbot_used=actual_chatbot,
            answer=answer,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Feedback endpoint: collect user feedback on answers.
    
    If positive: log success
    If negative: store corrected labels for future fine-tuning
    """
    try:
        feedback_data = {
            "question": request.question,
            "predicted_domain": request.predicted_domain,
            "predicted_difficulty": request.predicted_difficulty,
            "chatbot_used": request.chatbot_used,
            "response": request.response,
            "feedback_positive": request.feedback_positive,
            "corrected_domain": request.corrected_domain,
            "corrected_difficulty": request.corrected_difficulty
        }
        
        # Save feedback
        storage.save_feedback(feedback_data)
        
        if request.feedback_positive:
            message = "Thank you for your positive feedback!"
            logger.info("Positive feedback logged")
        else:
            message = "Thank you for your feedback. We'll use it to improve our system."
            logger.info(f"Negative feedback logged with corrections: Domain={request.corrected_domain}, Difficulty={request.corrected_difficulty}")
        
        return FeedbackResponse(
            message=message,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving feedback: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get feedback statistics."""
    try:
        all_feedback = storage.get_all_feedback()
        negative_feedback = storage.get_negative_feedback()
        
        total_feedback = len(all_feedback)
        positive_count = sum(1 for fb in all_feedback if fb.get('feedback_positive', False))
        negative_count = len(negative_feedback)
        
        return {
            "total_feedback": total_feedback,
            "positive_feedback": positive_count,
            "negative_feedback": negative_count,
            "positive_rate": positive_count / total_feedback if total_feedback > 0 else 0,
            "negative_feedback_items": negative_feedback[-10:]  # Last 10 negative feedbacks
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
