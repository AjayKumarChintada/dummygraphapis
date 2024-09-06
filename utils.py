import pandas as pd

def calculate_cash_in_flow_by_account(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Inflow']
    cash_in_flow_by_account = cash_in_data.groupby('Account')['Amount'].sum()
    return cash_in_flow_by_account.to_dict()

def calculate_cash_flow_by_activity(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    cash_flow_by_activity = filtered_data.groupby('Account Category')['Amount'].sum()
    return cash_flow_by_activity.to_dict()

def calculate_cash_flow_trend(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    inflow_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Inflow']
    outflow_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Outflow']
    inflow_trend = inflow_data.groupby(inflow_data['Date'].dt.to_period('M'))['Amount'].sum()
    outflow_trend = outflow_data.groupby(outflow_data['Date'].dt.to_period('M'))['Amount'].sum()
    inflow_trend.index = inflow_trend.index.astype(str)
    outflow_trend.index = outflow_trend.index.astype(str)
    
    cash_flow_trend = {
        'Inflow': inflow_trend.to_dict(),
        'Outflow': outflow_trend.to_dict()
    }
    
    return cash_flow_trend

def calculate_cash_in_flow_by_customer(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Inflow']
    cash_in_flow_by_customer = cash_in_data.groupby('Customer')['Amount'].sum()
    return cash_in_flow_by_customer.to_dict()

def calculate_cash_out_flow_by_vendor(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Outflow']
    cash_out_flow_by_vendor = cash_in_data.groupby('Vendor')['Amount'].sum()
    return cash_out_flow_by_vendor.to_dict()

def calculate_cash_out_flow_by_account(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Outflow']
    cash_out_flow_by_account = cash_in_data.groupby('Account')['Amount'].sum()
    return cash_out_flow_by_account.to_dict()


def total_cash_in(data,start_date,end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= pd.to_datetime(start_date, dayfirst=False)) &
                         (data['Date'] <= pd.to_datetime(end_date, dayfirst=False))]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Inflow']
    total_cash_inflow = cash_in_data['Amount'].sum()
    return total_cash_inflow

def total_cash_out(data,start_date,end_date):
    data['Date'] = pd.to_datetime(data['Date'])
    filtered_data = data[(data['Date'] >= pd.to_datetime(start_date, dayfirst=False)) &
                         (data['Date'] <= pd.to_datetime(end_date, dayfirst=False))]
    cash_in_data = filtered_data[filtered_data['Cash Flow Type'] == 'Cash Outflow']
    total_cash_outflow = cash_in_data['Amount'].sum()
    return total_cash_outflow


def total_net_cash(data,start_date,end_date):
    net_cash = total_cash_in(data,start_date,end_date) + total_cash_out(data,start_date,end_date)
    return net_cash

def cash_in_for_customer(data,start_date,end_date):
    return total_cash_in(data,start_date,end_date) / 10


def cash_out_for_customer(data,start_date,end_date):
    return total_cash_out(data,start_date,end_date) / 10



    