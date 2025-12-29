# LSTM Financial Model - Specification

## Overview
Build a Long Short-Term Memory (LSTM) neural network model for financial time series prediction using TensorFlow and the APEXE3 MCP server API endpoints for data retrieval.

## Project Structure
```
FinancialMLUseCase/
├── data_fetcher.py          # Fetch financial data from APEXE3 API
├── data_preprocessor.py     # Preprocess and prepare data for LSTM
├── model_builder.py         # Build and configure LSTM model
├── trainer.py               # Train the model
├── predictor.py             # Make predictions
├── evaluator.py             # Evaluate model performance
├── config.py                # Configuration parameters
├── requirements.txt         # Python dependencies
└── main.py                  # Main execution script
```

## Prerequisites
- Python 3.8+
- TensorFlow 2.x
- NumPy
- Pandas
- Scikit-learn
- Requests

## Step-by-Step Implementation

DO NOT CLONE THE https://github.com/apexe3/api-examples repository

### Step 1: Setup Configuration (config.py)
Create a configuration file with the following parameters:
- API base URL: `https://alicev2.apexe3.ai/alice/apexe3/datahub/api`
- Default stock symbol S&P 500 (e.g., "^GSPC")
- Date range for training data
- LSTM hyperparameters:
  - Sequence length (lookback window)
  - Number of LSTM units
  - Dropout rate
  - Number of epochs
  - Batch size
  - Learning rate
- Train/test split ratio

### Step 2: Data Fetcher (data_fetcher.py)
Implement a class to fetch historical price data from APEXE3 API:

**API Endpoint:**
```
GET https://alicev2.apexe3.ai/alice/apexe3/datahub/api/asset_price_history/{symbol}
Query Parameters:
  - start_date: YYYY-MM-DD (optional)
  - end_date: YYYY-MM-DD (optional)
```

**Requirements:**
- Create a `DataFetcher` class
- Method `fetch_historical_data(symbol, start_date, end_date)`:
  - Make HTTP GET request to APEXE3 API
  - Handle API errors and network issues
  - Return JSON response with OHLCV data
  - Parse response into pandas DataFrame
  - Validate data integrity
- Method `get_sp500_symbols()`:
  - Fetch S&P 500 symbols from APEXE3 API
  - Return list of available symbols

**Expected Response Format:**
```json
{
  "symbol": "^GSPC",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "data": [
    {
      "date": "YYYY-MM-DD",
      "open": number,
      "high": number,
      "low": number,
      "close": number,
      "adj_close": number,
      "volume": integer
    }
  ]
}
```

### Step 3: Data Preprocessor (data_preprocessor.py)
Implement a class to prepare data for LSTM training:

**Requirements:**
- Create a `DataPreprocessor` class
- Method `clean_data(df)`:
  - Handle missing values (forward fill or drop)
  - Remove outliers using IQR method
  - Ensure chronological order
- Method `create_features(df)`:
  - Calculate technical indicators:
    - Moving averages (5, 10, 20, 50 days)
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Bollinger Bands
    - Volume changes
  - Create lag features
- Method `normalize_data(df)`:
  - Use MinMaxScaler for feature scaling
  - Fit on training data only
  - Transform both train and test data
- Method `create_sequences(data, sequence_length)`:
  - Create sliding window sequences for LSTM
  - Input shape: (samples, sequence_length, features)
  - Target: next day's closing price
- Method `split_data(X, y, test_ratio)`:
  - Split into train and test sets
  - Maintain temporal order (no shuffling)

### Step 4: Model Builder (model_builder.py)
Implement LSTM model architecture:

**Requirements:**
- Create a `ModelBuilder` class
- Method `build_lstm_model(input_shape, config)`:
  - Input layer matching sequence shape
  - First LSTM layer with return_sequences=True
  - Dropout layer for regularization
  - Second LSTM layer
  - Dropout layer
  - Dense layer(s) for feature extraction
  - Output layer (single neuron for regression)
  - Use Adam optimizer
  - Loss function: Mean Squared Error
  - Metrics: MAE, MSE
- Method `compile_model(model, learning_rate)`:
  - Compile with specified learning rate
- Method `get_model_summary(model)`:
  - Print model architecture

**Model Architecture:**
```
Input (sequence_length, n_features)
  ↓
LSTM(units=50, return_sequences=True)
  ↓
Dropout(0.2)
  ↓
LSTM(units=50)
  ↓
Dropout(0.2)
  ↓
Dense(25)
  ↓
Dense(1)
```

### Step 5: Trainer (trainer.py)
Implement model training logic:

**Requirements:**
- Create a `Trainer` class
- Method `train_model(model, X_train, y_train, config)`:
  - Train with early stopping callback
  - Use validation split (e.g., 0.2)
  - Implement learning rate reduction on plateau
  - Save training history
- Method `save_model(model, filepath)`:
  - Save trained model in HDF5 format
- Method `load_model(filepath)`:
  - Load saved model
- Method `plot_training_history(history)`:
  - Visualize training and validation loss
  - Plot MAE over epochs

**Callbacks:**
- EarlyStopping: patience=10, restore_best_weights=True
- ReduceLROnPlateau: factor=0.5, patience=5

### Step 6: Predictor (predictor.py)
Implement prediction functionality:

**Requirements:**
- Create a `Predictor` class
- Method `predict(model, X_test)`:
  - Generate predictions on test data
  - Return predicted values
- Method `predict_next_day(model, last_sequence)`:
  - Predict next day's price
  - Use most recent sequence
- Method `inverse_transform_predictions(predictions, scaler)`:
  - Convert scaled predictions back to original scale
- Method `plot_predictions(actual, predicted)`:
  - Visualize actual vs predicted prices
  - Calculate and display prediction error

### Step 7: Evaluator (evaluator.py)
Implement model evaluation metrics:

**Requirements:**
- Create an `Evaluator` class
- Method `calculate_metrics(y_true, y_pred)`:
  - Mean Absolute Error (MAE)
  - Mean Squared Error (MSE)
  - Root Mean Squared Error (RMSE)
  - Mean Absolute Percentage Error (MAPE)
  - R-squared (R²)
- Method `calculate_directional_accuracy(y_true, y_pred)`:
  - Percentage of correct directional predictions
- Method `generate_evaluation_report(metrics)`:
  - Create an advanced dashboard with all metrics
  - Include an actual price vs predicted price chart using the actual price units
  - Include model performance interpretation

### Step 8: Main Execution Script (main.py)
Create the main orchestration script:

**Requirements:**
- Import all modules
- Load configuration
- Execute pipeline:
  1. Fetch data from APEXE3 API
  2. Preprocess data
  3. Split into train/test
  4. Build LSTM model
  5. Train model
  6. Evaluate on test set
  7. Make predictions
  8. Generate report
  9. Save model and results
- Handle errors gracefully
- Log progress and results

**Execution Flow:**
```python
def main():
    # Load config
    config = load_config()
    
    # Fetch data
    fetcher = DataFetcher()
    df = fetcher.fetch_historical_data(config.symbol, config.start_date, config.end_date)
    
    # Preprocess
    preprocessor = DataPreprocessor()
    df_clean = preprocessor.clean_data(df)
    df_features = preprocessor.create_features(df_clean)
    X, y = preprocessor.create_sequences(df_features, config.sequence_length)
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y, config.test_ratio)
    
    # Build model
    builder = ModelBuilder()
    model = builder.build_lstm_model((X_train.shape[1], X_train.shape[2]), config)
    
    # Train
    trainer = Trainer()
    history = trainer.train_model(model, X_train, y_train, config)
    
    # Evaluate
    predictor = Predictor()
    y_pred = predictor.predict(model, X_test)
    evaluator = Evaluator()
    metrics = evaluator.calculate_metrics(y_test, y_pred)
    
    # Save results
    trainer.save_model(model, 'lstm_model.h5')
    evaluator.generate_evaluation_report(metrics)
```

### Step 9: Requirements File (requirements.txt)
Create requirements.txt with:
```
tensorflow>=2.10.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
requests>=2.26.0
matplotlib>=3.4.0
```

## API Integration Notes

### APEXE3 API Endpoints Used:
1. **Historical Price Data:**
   - Endpoint: `/asset_price_history/{symbol}`
   - Method: GET
   - Parameters: start_date, end_date
   - Returns: OHLCV data

2. **S&P 500 Symbols:**
   - Endpoint: `/sp500_symbols`
   - Method: GET
   - Returns: List of S&P 500 tickers

### Error Handling:
- Implement retry logic for API failures
- Handle rate limiting
- Validate API responses
- Log all API calls and errors
- Include a .gitignore which includes the venv entry

## Data Considerations

### Feature Engineering:
- Use closing price as primary target
- Include volume as feature
- Add technical indicators for better predictions
- Consider market sentiment if available

### Time Series Specifics:
- Maintain temporal order
- No data leakage from future
- Use walk-forward validation for robustness
- Consider multiple time horizons (1-day, 5-day, 10-day)

## Model Optimization

### Hyperparameter Tuning:
- Sequence length: 30-90 days
- LSTM units: 32-128
- Dropout: 0.1-0.3
- Learning rate: 0.001-0.0001
- Batch size: 16-64

### Regularization:
- Dropout layers
- L2 regularization
- Early stopping
- Batch normalization

## Testing and Validation

### Validation Strategy:
- Time-based split (not random)
- Walk-forward validation
- Out-of-sample testing
- Multiple stock symbols

### Performance Benchmarks:
- MAPE < 5% for good model
- Directional accuracy > 55%
- Consistent performance across symbols

## Deployment Considerations

### Model Persistence:
- Save model architecture and weights
- Store scaler parameters
- Version control models
- Document model performance

### Monitoring:
- Track prediction accuracy over time
- Monitor model drift
- Retrain periodically with new data
- Alert on performance degradation

## Future Enhancements

1. **Multi-Stock Models:**
   - Train on multiple stocks
   - Use stock embeddings
   - Transfer learning

2. **Advanced Features:**
   - News sentiment analysis
   - Social media data
   - Macroeconomic indicators
   - Sector correlations

3. **Model Variants:**
   - GRU networks
   - Attention mechanisms
   - Transformer models
   - Ensemble methods

4. **Production Features:**
   - Real-time inference API
   - Batch prediction pipeline
   - Automated retraining
   - A/B testing framework

## Success Criteria

- [ ] Successfully fetch data from APEXE3 API
- [ ] Clean and preprocess financial data
- [ ] Build functional LSTM model
- [ ] Train model without overfitting
- [ ] Achieve reasonable prediction accuracy
- [ ] Generate comprehensive evaluation report
- [ ] Save and load model correctly
- [ ] Handle errors gracefully
- [ ] Document code and usage
- [ ] Create reproducible pipeline
