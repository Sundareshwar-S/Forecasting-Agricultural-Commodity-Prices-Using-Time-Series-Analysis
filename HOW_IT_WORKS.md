# How the Agricultural Price Forecasting System Works

## 🎯 Goal
**Predict commodity prices for the entire year 2026** using actual 2025 price data.

---

## 📊 What the Graph Shows

### Four Different Lines:
1. **Blue Line (Historical 2025 Data)**
   - Real prices from January to December 2025
   - This is what we learn from
   - The baseline of our prediction

2. **Green Dashed Line (Test Predictions)**
   - Model's prediction on 20% of 2025 data
   - Shows how accurate the model is
   - If this matches blue line closely = model is good

3. **Red Line (Year 2026 Forecast)**
   - The ACTUAL PREDICTION you care about
   - Shows predicted prices for all 365 days of 2026
   - This is the future!

4. **Light Red Shaded Area (Confidence Interval)**
   - The range where price is likely to be
   - 95% confidence = 95% chance actual price falls here
   - Shows uncertainty of predictions

---

## 🔧 How the System Works (Step by Step)

### Step 1: Data Extraction
```
Read from MongoDB → Get Carrot prices for all markets
```
- Connects to MongoDB database
- Retrieves 99,307+ price records for selected commodity
- Example: Green Chilli prices from different markets

### Step 2: Data Cleaning
```
Raw Data → Remove errors → Prepare for analysis
```
- Remove missing values
- Convert dates to proper format
- Remove duplicates
- Remove unrealistic prices (like ₹100,000 which is wrong)
- Average prices across markets
- Fill missing days with interpolation

### Step 3: Visualization
```
Display historical price trend to understand pattern
```
- Shows price movement over time
- Helps identify trends and seasonality

### Step 4: Moving Average
```
Smooth the data to see overall trend (ignoring daily noise)
```
- 7-day moving average (weekly trend)
- 14-day moving average (bi-weekly trend)
- Helps identify uptrends and downtrends

### Step 5: Outlier Detection
```
Find unusual price spikes that don't fit pattern
```
- Uses IQR (Interquartile Range) method
- Red dots = unusual prices
- Blue dots = normal prices

### Step 6: Forecasting (THE MAIN PART)
```
2025 Historical Data → SARIMA Model → 2026 Predictions
```

**What is SARIMA?**
- **S** = Seasonal (repeats in patterns, like weekly/monthly)
- **A** = Auto-Regressive (past prices affect future prices)
- **R** = Integrated (handles non-stationary data)
- **I** = Moving Average (uses past errors)
- **M** = Multivariate (multiple variables)

**How Does It Work?**

1. **Train-Test Split** (80% - 20%)
   - 80% of 2025 = 291 days for training
   - 20% of 2025 = 73 days for testing
   - This simulates real-world: train on old data, predict new data

2. **Auto Parameter Tuning**
   - Tests hundreds of SARIMA combinations
   - Picks the best one using AIC score
   - Example: SARIMA(2,1,1) x (1,0,1,7)
   
   Meaning:
   - (2,1,1) = Non-seasonal components
   - (1,0,1,7) = Seasonal components (7 days for weekly pattern)

3. **Model Training**
   - Learns patterns from all 2025 data
   - Understands how prices change
   - Memorizes weekly seasonality (prices vary by day of week)

4. **Validation on Test Data**
   - Predicts the 73 test days
   - Compares with actual prices
   - Calculates accuracy metrics

5. **Year 2026 Prediction**
   - Forecasts 365 days into future
   - Extrapolates patterns to 2026
   - Generates confidence intervals (prediction uncertainty)

---

## 📈 Accuracy Metrics Explained

### RMSE (Root Mean Squared Error)
- **What**: Average error magnitude in rupees
- **Example**: ₹425.66 means prediction is typically off by ₹425.66
- **Lower is Better**: ✅ < ₹500 = Excellent

### MAE (Mean Absolute Error)
- **What**: Simple average deviation
- **Example**: ₹308.75 typical difference from actual price
- **Lower is Better**: ✅ < ₹300 = Excellent

### MAPE (Mean Absolute Percentage Error)
- **What**: Error as a percentage of actual price
- **Example**: 8.85% = Predictions off by 8.85% on average
- **Accuracy**: 100% - 8.85% = **91.15% accurate**
- **How to Interpret**:
  - 0-10% = Excellent ✅
  - 10-20% = Good
  - 20-50% = Fair
  - 50%+ = Poor

---

## 🎓 Why This Matters

### For Farmers:
- Know expected prices before planting
- Plan better crop selection
- Time sales strategically

### For Traders:
- Anticipate price movements
- Make informed buying/selling decisions
- Manage inventory better

### For Policymakers:
- Understand market trends
- Plan subsidies/taxes
- Make policy decisions

---

## 📊 Reading the Results Page

### Top Section (Purple Cards):
Shows **Model Accuracy Metrics**
- RMSE, MAE, MAPE
- Lower numbers = better prediction

### Middle Section (Blue Box):
Shows **Model Information**
- Which SARIMA model was used
- How many training & test samples
- Explanation of accuracy

### Charts (4 Total):
1. **Price Trend** - 2025 actual prices
2. **Moving Average** - Smoothed trends
3. **Outlier Detection** - Unusual prices
4. **Price Forecast with CI** - 2026 predictions

### Bottom Section (Table):
Shows **365 Predicted Prices**
- Day number
- Predicted price (red line in graph)
- Min bound (95% CI lower)
- Max bound (95% CI upper)

---

## 🔍 Example: How to Read a Prediction

**Day 45 (February 14, 2026):**
- Predicted Price: ₹3,215.89
- Lower Bound: ₹2,428.26
- Upper Bound: ₹4,003.52

**Interpretation:** "On Feb 14, 2026, Green Chilli should cost around ₹3,215, but could reasonably be anywhere between ₹2,428 and ₹4,003 with 95% confidence."

---

## ⚙️ Technical Summary

```
MongoDB (Raw Data)
    ↓
Data Extraction (99,307 records)
    ↓
Data Cleaning (Remove errors, aggregate)
    ↓
Time Series Analysis (364 days of 2025)
    ↓
Auto ARIMA (Find best SARIMA model)
    ↓
Train-Test Split (291 train, 73 test)
    ↓
Model Validation (RMSE, MAE, MAPE)
    ↓
Year 2026 Forecast (365 days, with 95% CI)
    ↓
Visualization & Results
```

---

## ❓ FAQ

**Q: Why only 364 days of 2025 data?**
A: After data cleaning, we have 364 actual days (some days have no trades)

**Q: Why 365-day forecast?**
A: 2026 is not a leap year (365 days). Forecast starts from last date of 2025 data.

**Q: Why 95% confidence interval?**
A: This is standard in statistics. 95% is a good balance between precision and confidence.

**Q: Can I trust 365-day forecast?**
A: Long forecasts have wider confidence intervals (more uncertainty). Near-term predictions (0-30 days) are more reliable than far-future ones (300+ days).

**Q: What if MAPE is 20%?**
A: Still acceptable for commodity prices. Agricultural markets are volatile. 20% means 80% accuracy on average.

**Q: Why green dashed line matters?**
A: It proves the model works. If green matches blue closely (in test period), the red line (2026) is trustworthy.

---

**Updated**: March 10, 2026  
**System Status**: ✅ Active  
**Forecast Accuracy**: Excellent (MAPE < 10%)
