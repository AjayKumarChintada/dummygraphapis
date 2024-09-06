# main.py

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
import numpy as np
import random
from fastapi.middleware.cors import CORSMiddleware
from utils import *
from datageneration import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

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

@app.post("/charts/bar", response_model=List[BarChartData],tags =["Dummy Grahps"])
def get_bar_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_bar_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/line", response_model=List[LineChartData],tags =["Dummy Grahps"])
def get_line_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_line_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/histogram", response_model=List[HistogramData],tags =["Dummy Grahps"])
def get_histogram_data(request: HistogramRequest):
    return generate_histogram_data(request.num_bins)

@app.post("/charts/scatter", response_model=List[ScatterData],tags =["Dummy Grahps"])
def get_scatter_data(request: ScatterRequest):
    return generate_scatter_data(request.num_points)

@app.post("/charts/candlestick", response_model=List[CandlestickData],tags =["Dummy Grahps"])
def get_candlestick_data(request: CandlestickRequest):
    try:
        start_date = datetime.datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_candlestick_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

@app.post("/charts/pie", response_model=List[PieChartData],tags =["Dummy Grahps"])
def get_pie_chart_data(request: PieRequest):
    return generate_pie_chart_data(request.num_segments)

@app.post("/charts/area", response_model=List[AreaChartData],tags =["Dummy Grahps"])
def get_area_chart_data(request: DateRangeRequest):
    try:
        start_date = datetime.datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(request.end_date, "%Y-%m-%d")
        return generate_area_chart_data(start_date, end_date, request.num_points)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")


####### real apis from data ############


data = pd.read_excel('finstackdata.xlsx')

# Helper function to convert date strings to datetime
def convert_dates(start_date: str, end_date: str):
    return pd.to_datetime(start_date, dayfirst=False), pd.to_datetime(end_date, dayfirst=False)

# Pydantic Models for request validation
class DateRangeRequest(BaseModel):
    start_date: str
    end_date: str

# API Endpoints

@app.post("/cashflow/inflow/account",tags = ["Finstack data"])
def get_cash_inflow_by_account(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_in_flow_by_account(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/outflow/account",tags = ["Finstack data"])
def get_cash_outflow_by_account(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_out_flow_by_account(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/inflow/customer",tags = ["Finstack data"])
def get_cash_inflow_by_customer(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_in_flow_by_customer(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/outflow/vendor",tags = ["Finstack data"])
def get_cash_outflow_by_vendor(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_out_flow_by_vendor(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/trend",tags = ["Finstack data"])
def get_cash_flow_trend(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_flow_trend(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/activity",tags = ["Finstack data"])
def get_cash_flow_by_activity(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = calculate_cash_flow_by_activity(data, start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/total_inflow", tags = ["Finstack data"])
def get_total_cash_inflow(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = total_cash_in(data, start_date, end_date)
        return {"total_cash_inflow": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/total_outflow", tags = ["Finstack data"])
def get_total_cash_outflow(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = total_cash_out(data, start_date, end_date)
        return {"total_cash_outflow": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/net", tags = ["Finstack data"])
def get_total_net_cash(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = total_net_cash(data, start_date, end_date)
        return {"net_cash_flow": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/customer/inflow", tags = ["Finstack data"])
def get_cash_inflow_for_customer(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = cash_in_for_customer(data, start_date, end_date)
        return {"customer_cash_inflow": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cashflow/customer/outflow",tags = ["Finstack data"])
def get_cash_outflow_for_customer(request: DateRangeRequest):
    try:
        start_date, end_date = convert_dates(request.start_date, request.end_date)
        result = cash_out_for_customer(data, start_date, end_date)
        return {"customer_cash_outflow": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))