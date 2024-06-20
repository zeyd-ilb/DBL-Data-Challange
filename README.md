
# DBL Data Challenge

Welcome to the DBL Data Challenge repository! This project contains various tools and scripts for data processing and analysis, specifically focusing on airline data.

## Table of Contents

- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)

## Project Overview

This repository is designed to help with various data challenges, including data aggregation, cleaning, and analysis using machine learning models. It includes demo codes for different tasks and example data to get you started.

## Folder Structure

The repository is organized as follows:

- **Demo Codes**: Contains scripts for different tasks.
  - `Aggregations`: Scripts for data aggregation.
  - `ChatBot`: Code for chatbot functionalities.
  - `Cleaning`: Folder that includes scripts for data cleaning.
  - `MongoCompound.py`: MongoDB compound queries.
  - `RoBERTa_compound.py`: RoBERTa model scripts. It makes compound sentiment scores for selected text.
  - `create_chains.py`: Script for creating the conversation chains.
  - `cumulative scores per reply.py`: Script for calculating cumulative scores before a reply from the airline.
  - `import_jsons.py`: Script for importing JSON files into mongodb. Usefull to import multiple json files at once.
  - `vader.py`: VADER sentiment analysis script.
  - `txt fix.py`:  Use it on the ouput of `cumulative_scores_per_reply.py` script. Keeps only the chains that have certain length in the txt file.
  - `txt to csv.py`: Use it on the ouput of `txt fix.py` script. Convert txt file to proper csv.

## Usage of Sentiment Scores 

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
![WhatsApp Görsel 2024-06-11 saat 16 00 49_8e0fa7b2](https://github.com/zeyd-ilb/DBL-Data-Challange/assets/61659041/6afb6c15-7617-4fed-b3fc-aa3259d7634a)
