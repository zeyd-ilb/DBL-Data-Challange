First get the cleaned data from the link below. Import the data to mongodb with "import_jsons_w_prepocess.py". After import is done run "duplicate_detele.py". 
Cleaned Data link: https://drive.google.com/file/d/1-6xE6I_2iiRiGZ-A9UX846D8KEDvT-1J/view

If you want to clean the data by yourself:
  1) Run "cleaning.py" on the raw data. This will clean the data. Make sure you change the directory path to where you have your data stored.
  2) Import this cleaned data to mongodb using "import_jsons.py"
  3) Configure the file names in "find_retweets.py" then run
  4) You should now be able to find "orphan_RTs_ids.txt" in the directory where you are running this code. This text file stores the IDs of retweets that don't have an original tweet in the data.
  5) Then run "cleaning.py" by replacing the path to "orphan_RTs_ids.txt"
  6) After the cleaning is done repeat step 2 with the new cleaned data
  7) After import is done run "duplicate_delete.py" on mongodb for the new cleaned data.

![WhatsApp Görsel 2024-06-11 saat 16 00 49_f7b6d4f0](https://github.com/zeyd-ilb/DBL-Data-Challange/assets/61659041/b3fbdca5-797e-4588-b607-db8c4796b863)
