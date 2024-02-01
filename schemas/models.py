from pydantic import *

class betBody(BaseModel):
    player: str
    bet: str