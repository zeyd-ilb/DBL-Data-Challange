
# DBL Data Challenge

Welcome to the DBL Data Challenge repository! This project contains various tools and scripts for data processing and analysis, specifically focusing on airline data.

## Table of Contents

- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)

## Project Overview

This repository is designed to help with various data challenges, including data aggregation, cleaning, and analysis using machine learning models. It includes demo codes for our ChatBot and making the visualisations that can be found in our poster.

## Folder Structure

The repository is organized as follows:
  - `Aggregations`: Scripts for data aggregation.
  - `ChatBot`: Code for chatbot functionalities.
  - `Cleaning`: Folder that includes scripts for data cleaning.
  - `Sentiment-Analysis`: Folder that includes scripts for sentiment analysis.
  - `Sentiment Analysis Graph`: Code for creating testing sentiment evolution and creating a graph for it.
The four folders above have respective README files explaining the scripts they contain.


## [Usage of Sentiment Scores](Demo Codes)

This part explains how to do a sentiment evolution on conversation chains. Our definition of evoulution is comparing the sentiment scores before an airline reponse with after the response. An example graph could look like the one in below:  

![image](https://github.com/zeyd-ilb/DBL-Data-Challange/assets/61659041/bb2dcea1-0d63-433c-81f0-2a4d1cd68a23)

**Steps**:

- First adjust the database variables, airline id's, output file name and the time frame that you want your graph to include in the `cumulative_scores_per_reply.py` script. Then run the script and get the output text file. 
- In `txt fix.py`, adjust the input and output file names (as you wish) and the desired lenght of the conversation chains. The input must be the ouput file of the `cumulative_scores.py` script.
- In `txt to csv.py`, adjust the input file name. The input must be the ouput file of `txt fix.py`
- Then you can upload the csv file to excel or google sheets, and create the charts that you wish. 

## Installation

To use the scripts in this repository, you need to have Python installed. Clone the repository and install the required dependencies.

```sh
git clone https://github.com/yourusername/DBL-Data-Challange.git
cd DBL-Data-Challange
pip install -r requirements.txt
```
## Flow Chart for Cleaning

![cleaning py (1)](https://github.com/zeyd-ilb/DBL-Data-Challange/assets/61659041/83b3eb02-6141-4a4b-93b3-c3e154cebd05)
