import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp  # Make sure to import these
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

# (Include the BlackScholes class definition here)

class BlackScholesCalculator:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(
        self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike) +
            (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
            ) / (
                volatility * sqrt(time_to_maturity)
            )
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
        ) - current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

        # GREEKS
        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Gamma
        self.call_gamma = norm.pdf(d1) / (
            strike * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        return call_price, put_price

# Function to generate heatmaps
# ... your existing imports and BlackScholes class definition ...


# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Black-Scholes Model Calculator")
    st.write("`Created by:`")
    Github_url = "https://github.com/TayKaunda"
    st.markdown(f'<a href="{Github_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="data:image/jpeg;base64,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" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Tay Kaunda`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)



def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholesCalculator(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            bs_temp.calculate_prices()
            call_prices[i, j] = bs_temp.call_price
            put_prices[i, j] = bs_temp.put_price
    
    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')
    
    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    
    return fig_call, fig_put


# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values
bs_model = BlackScholesCalculator(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)