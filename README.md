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
  - `Cleaning`: Scripts for data cleaning.
  - `MongoCompound.py`: MongoDB compound queries.
  - `RoBERTa_compound.py`: RoBERTa model scripts. It makes compound sentiment scores for selected text.
  - `create_chains.py`: Script for creating the conversation chains.
  - `cumulative scores per reply.py`: Script for calculating cumulative scores before a reply from the airline.
  - `import_jsons.py`: Script for importing JSON files into mongodb.
  - `vader.py`: VADER sentiment analysis script.
  - `txt fix.py`:  Use it on the ouput of `cumulative_scores_per_reply.py` script. Keeps only the chains that have certain length in the txt file.
  - `txt to csv.py`: Use it on the ouput of `txt fix.py` script. Convert txt file to proper csv.

- **Example-data**: Contains example data files.
  - `airlines-1558527599826.json`: Example dataset for analysis.

## Usage of Sentiment Scores 


## Installation

To use the scripts in this repository, you need to have Python installed. Clone the repository and install the required dependencies.

```sh
git clone https://github.com/yourusername/DBL-Data-Challange.git
cd DBL-Data-Challange
pip install -r requirements.txt
```
