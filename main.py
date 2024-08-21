# main.py

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import numpy as np
import random
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Data generation functions
def generate_date_range(start_date: datetime, end_date: datetime, num_points: int):
    delta = (end_date - start_date) // num_points
    return [start_date + i * delta for i in range(num_points)]

def seasonal_trend(date: datetime) -> float:
    """Simulate a seasonal trend with sinusoidal variation."""
    day_of_year = date.timetuple().tm_yday
    return 100 + 50 * np.sin(2 * np.pi * day_of_year / 365)

def generate_bar_chart_data(start_date: datetime, end_date: datetime, num_points: int):
    dates = generate_date_range(start_date, end_date, num_points)
    data = []
    for date in dates:
        base_value = seasonal_trend(date)
        value = base_value + random.uniform(-30, 30)
        data.append({"date": date.strftime("%Y-%m-%d"), "value": max(0, round(value))})
    return data

def generate_line_chart_data(start_date: datetime, end_date: datetime, num_points: int):
    dates = generate_date_range(start_date, end_date, num_points)
    data = [{"date": date.strftime("%Y-%m-%d"), "value": seasonal_trend(date) + random.uniform(-20, 20)} for date in dates]
    return data

def generate_histogram_data(num_bins: int):
    bins = [f"{i*10}-{(i+1)*10}" for i in range(num_bins)]
    frequencies = [random.randint(0, 100) for _ in range(num_bins)]
    return [{"bin": bin, "frequency": freq} for bin, freq in zip(bins, frequencies)]

def generate_scatter_data(num_points: int):
    return [{"x": random.uniform(0, 100), "y": random.uniform(0, 100)} for _ in range(num_points)]

def generate_candlestick_data(start_date: datetime, end_date: datetime, num_points: int):
    dates = generate_date_range(start_date, end_date, num_points)
    data = []
    for date in dates:
        open_price = random.uniform(100, 200)
        high_price = open_price + random.uniform(0, 10)
        low_price = open_price - random.uniform(0, 10)
        close_price = random.uniform(low_price, high_price)
        data.append({"date": date.strftime("%Y-%m-%d"), "open": open_price, "high": high_price, "low": low_price, "close": close_price})
    return data

def generate_pie_chart_data(num_segments: int):
    labels = [f"Segment {i+1}" for i in range(num_segments)]
    values = [random.randint(10, 100) for _ in range(num_segments)]
    total = sum(values)
    return [{"label": label, "value": round((value / total) * 100, 2)} for label, value in zip(labels, values)]

def generate_area_chart_data(start_date: datetime, end_date: datetime, num_points: int):
    dates = generate_date_range(start_date, end_date, num_points)
    data = [{"date": date.strftime("%Y-%m-%d"), "value": seasonal_trend(date) + random.uniform(-15, 15)} for date in dates]
    return data

# Pydantic models for request and response
class DateRangeRequest(BaseModel):
    start_date: str
    end_date: str
    num_points: Optional[int] = 12

class HistogramRequest(BaseModel):
    num_bins: int

class ScatterRequest(BaseModel):
    num_points: int

class CandlestickRequest(BaseModel):
    start_date: str
    end_date: str
    num_points: Optional[int] = 12

class PieRequest(BaseModel):
    num_segments: int

class BarChartData(BaseModel):
    date: str
    value: int

class LineChartData(BaseModel):
    date: str
    value: float

class HistogramData(BaseModel):
    bin: str
    frequency: int

class ScatterData(BaseModel):
    x: float
    y: float

class CandlestickData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float

class PieChartData(BaseModel):
    label: str
    value: float

class AreaChartData(BaseModel):
    date: str
    value: float

@app.post("/charts/bar", response_model=List[BarChartData])
def get_bar_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_bar_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/line", response_model=List[LineChartData])
def get_line_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_line_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/histogram", response_model=List[HistogramData])
def get_histogram_data(request: HistogramRequest):
    return generate_histogram_data(request.num_bins)

@app.post("/charts/scatter", response_model=List[ScatterData])
def get_scatter_data(request: ScatterRequest):
    return generate_scatter_data(request.num_points)

@app.post("/charts/candlestick", response_model=List[CandlestickData])
def get_candlestick_data(request: CandlestickRequest):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_candlestick_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/pie", response_model=List[PieChartData])
def get_pie_chart_data(request: PieRequest):
    return generate_pie_chart_data(request.num_segments)

@app.post("/charts/area", response_model=List[AreaChartData])
def get_area_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_area_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
