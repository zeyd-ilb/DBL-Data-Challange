  - `create_chains.py`: Script for creating the conversation chains.
  - `cumulative scores per reply.py`: Script for calculating cumulative scores before a reply from the airline.
  - `txt fix.py`:  Use it on the ouput of `cumulative_scores_per_reply.py` script. Keeps only the chains that have certain length in the txt file.
  - `txt to csv.py`: Use it on the ouput of `txt fix.py` script. Convert txt file to proper csv.

## Usage of Sentiment Scores 
This part explains how to do a sentiment evolution on conversation chains. Our definition of evoulution is comparing the sentiment scores before an airline reponse with after the response. An example graph could look like the one in below:  

![image](https://github.com/zeyd-ilb/DBL-Data-Challange/assets/61659041/bb2dcea1-0d63-433c-81f0-2a4d1cd68a23)

**Steps**:

- First adjust the database variables, airline id's, output file name and the time frame that you want your graph to include in the `cumulative_scores_per_reply.py` script. Then run the script and get the output text file. 
- In `txt fix.py`, adjust the input and output file names (as you wish) and the desired lenght of the conversation chains. The input must be the ouput file of the `cumulative_scores.py` script.
- In `txt to csv.py`, adjust the input file name. The input must be the ouput file of `txt fix.py`
- Then you can upload the csv file to excel or google sheets, and create the charts that you wish. 
