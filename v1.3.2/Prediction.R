library(forecast)
library(jsonlite)

# Read stock data from JSON file
stock_data <- jsonlite::fromJSON("stock_data.json")

# Extract closing prices
closing_prices <- stock_data$close

# Convert closing prices to numeric vector
closing_prices <- as.numeric(closing_prices)

# Fit ARIMA model
model <- auto.arima(closing_prices)
summary(model)

# Generate forecasts
forecast_horizon <- 1
f <- forecast(model, level = c(95), h = forecast_horizon)

# Plot forecast
plot(f)

# Write forecasted mean values to a file
write.table(f$mean, file = "prediction.txt", sep = "\t", row.names = FALSE, col.names = FALSE) # nolint: line_length_linter.

cat("Forecasted values written to 'prediction.txt'.\n")