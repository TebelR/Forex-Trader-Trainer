**Overview**

This application encompasses both a PyTorch ML model, and a simple environment for its training.
The goal is to develop a minimalistic GUI, which will allow one to work with financial data from a Forex Broker to train a model that can make financial forecasts and perform trading.

The interface contains 4 main frames - a terminal, a section for viewing data, a section for configuring an ML model, and a section for viewing indicators derived from selected data.

**Terminal**

The terminal is made from scratch and is not the main focus of this project. One might find it difficult to work with as it does not offer nearly as many quality-of-life things as the standard command terminal in various operating systems.

The following commands are implemented:

| Function name | Arguments                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| test          | None                                                               | Prints "Test passed" to the terminal if everything works as intended                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| list          | "accounts"                                                         | Prints out the entire list of available accounts that are currently stored in the DB                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| select        | "account #"                                                        | Selects an account to append to API calls. This is necessary for most API calls. # - is the index of the account that one wishes to select as per the array of accounts from the "list" command (0-based).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| fetch         | "accounts" or "prices 'pair' 'granularity' 'timeRange' 'fileName'" | Option 1 (account): fetches all accounts associated with the API token. Option 2 (prices): fetches price data about a currency pair with a certain candlestick granularity.                    'pair' - is the name of the currency pair. With Oanda, an acceptable pair looks like 'CAD_JPY'                    'granularity' - is the time step between candlesticks. Refer to Oanda for more information, but this                                     can be 'M' for months, 'W' for weeks, 'D' for days, 'H4' for 4 hour increments, etc.                    'timeRange' - this is a date and time in the format of DD:MM:YYYYTHH:MM:SS:SSSSSSSSSZ. All data from                                   the entered data up until today will be collected.                    'fileName' - this refers to the file where data should be stored in JSON format. This is in the 'data'                                  directory. |






**Data View Window**

-To be documented

**ML Window**

-To be documented

**Indicators Window**

-To be documented



Note that this repo does not have the API token uploaded. To run this yourself, you need to request a token from a FOREX Broker. This is developed using Oanda's API.