from fastapi import APIRouter, Query
from typing import List
from scraping_logic.scrape import *
from schemas.models import *




router = APIRouter()

@router.post('/nba/player_analyzation')
async def analyzePlayer(data: betBody):
    analyzation = await scrapeNBAStats(data)
    return {"Analyzation": analyzation}