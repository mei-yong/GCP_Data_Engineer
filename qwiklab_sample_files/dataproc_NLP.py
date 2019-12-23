
# Example Python file that runs NLP using Spark and one of the Google APIs

#!/usr/bin/env python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
  This program takes a sample text line of text and passes to a Natural Language Processing
  services, sentiment analysis, and processes the results in Python.
  
'''

import logging
import argparse
import json

import os
from googleapiclient.discovery import build

from pyspark import SparkContext
sc = SparkContext("local", "Simple App")

'''
You must set these values for the job to run.
'''
APIKEY="AIzaSyDQfGFSooY5LTas0RlvEJZ2inZcfPRf3RU"   # CHANGE
print(APIKEY)
PROJECT_ID="qwiklabs-gcp-8710406e275a5a84"  # CHANGE
print(PROJECT_ID) 
BUCKET="qwiklabs-gcp-8710406e275a5a84"   # CHANGE

## Wrappers around the NLP REST interface
def SentimentAnalysis(text):
    from googleapiclient.discovery import build
    lservice = build('language', 'v1beta1', developerKey=APIKEY)
    response = lservice.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text
            }
        }).execute()
    
    return response
## main
sampleline = 'There are places I remember, all my life though some have changed.'

# Calling the Natural Language Processing REST interface
#
results = SentimentAnalysis(sampleline)
# 
#  What is the service returning?
#
print("Function returns: ", type(results))
print(json.dumps(results, sort_keys=True, indent=4))


#################################################################################################

"""
1. This program uses Spark RDDs. It reads a small sample file and passes it to the Natural Language Processing service for Sentiment Analysis.

2. Post-processing of the returned data is done in the pipeline using transformations.

"""
#!/usr/bin/env python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
  This program reads a text file and passes to a Natural Language Processing
  service, sentiment analysis, and processes the results in Spark.
  
'''

import logging
import argparse
import json

import os
from googleapiclient.discovery import build

from pyspark import SparkContext
sc = SparkContext("local", "Simple App")

'''
You must set these values for the job to run.
'''
APIKEY="AIzaSyDQfGFSooY5LTas0RlvEJZ2inZcfPRf3RU"   # CHANGE
print(APIKEY)
PROJECT_ID="qwiklabs-gcp-8710406e275a5a84"  # CHANGE
print(PROJECT_ID) 
BUCKET="qwiklabs-gcp-8710406e275a5a84"   # CHANGE


## Wrappers around the NLP REST interface
def SentimentAnalysis(text):
    from googleapiclient.discovery import build
    lservice = build('language', 'v1beta1', developerKey=APIKEY)
    response = lservice.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text
            }
        }).execute()
    
    return response


## main
# We could use sc.textFiles(...)
#
#   However, that will read each line of text as a separate object.
#   And using the REST API to NLP for each line will rapidly exhaust the rate-limit quota 
#   producing HTTP 429 errors
#
#   Instead, it is more efficient to pass an entire document to NLP in a single call.
#
#   So we are using sc.wholeTextFiles(...)
#
#      This provides a file as a tuple.
#      The first element is the file pathname, and second element is the content of the file.
#
sample = sc.wholeTextFiles("gs://{0}/sampledata/road-not-taken.txt".format(BUCKET))
# Calling the Natural Language Processing REST interface
#
rdd1 = sample.map(lambda x: SentimentAnalysis(x[1]))
rdd2 =  rdd1.flatMap(lambda x: x['sentences'] )\
            .flatMap(lambda x: [(x['sentiment']['magnitude'], x['sentiment']['score'], [x['text']['content']])] )
  
results = rdd2.take(50)


for item in results:
  print('Magnitude= ',item[0],' | Score= ',item[1], ' | Text= ',item[2])


#################################################################################################

"""
1. This program builds on the previous one. Instead of reading a poem it is going to read an entire book. However, it could just as easily read and process an entire library.

2. Adds filter (in the pipeline) and sort (Python).

3. This gives a list of the lines in the book with the strongest sentiment, both positive and negative.

4. Now, this was just a book. Imagine how you could use this to sort through social media commentary. For example, consider the feedback left by customers on a shopping website. You could use this kind of data analysis to identify the most admired and most despised products.
"""

#!/usr/bin/env python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
  This program reads a text file and passes to a Natural Language Processing
  service, sentiment analysis, and processes the results in Spark.
  
'''
import logging
import argparse
import json
import os
from googleapiclient.discovery import build
from pyspark import SparkContext
sc = SparkContext("local", "Simple App")
'''
You must set these values for the job to run.
'''
APIKEY="AIzaSyDQfGFSooY5LTas0RlvEJZ2inZcfPRf3RU"   # CHANGE
print(APIKEY)
PROJECT_ID="qwiklabs-gcp-8710406e275a5a84"  # CHANGE
print(PROJECT_ID) 
BUCKET="qwiklabs-gcp-8710406e275a5a84"   # CHANGE
## Wrappers around the NLP REST interface
def SentimentAnalysis(text):
    from googleapiclient.discovery import build
    lservice = build('language', 'v1beta1', developerKey=APIKEY)
    response = lservice.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text
            }
        }).execute()
    
    return response
## main
# We could use sc.textFiles(...)
#
#   However, that will read each line of text as a separate object.
#   And using the REST API to NLP for each line will rapidly exhaust the rate-limit quota 
#   producing HTTP 429 errors
##   Instead, it is more efficient to pass an entire document to NLP in a single call.
#
#   So we are using sc.wholeTextFiles(...)
#
#      This provides a file as a tuple.
#      The first element is the file pathname, and second element is the content of the file.
#
sample = sc.wholeTextFiles("gs://{0}/sampledata/time-machine.txt".format(BUCKET))
# Calling the Natural Language Processing REST interface
#
# results = SentimentAnalysis(sampleline)
rdd1 = sample.map(lambda x: SentimentAnalysis(x[1]))
# The RDD contains a dictionary, using the key 'sentences' picks up each individual sentence
# The value that is returned is a list. And inside the list is another dictionary
# The key 'sentiment' produces a value of another list.
# And the keys magnitude and score produce values of floating numbers. 
#
rdd2 =  rdd1.flatMap(lambda x: x['sentences'] )\
            .flatMap(lambda x: [(x['sentiment']['magnitude'], x['sentiment']['score'], [x['text']['content']])] )
			
# First item in the list tuple is magnitude
# Filter on only the statements with the most intense sentiments
#
rdd3 =  rdd2.filter(lambda x: x[0]>.75)
results = sorted(rdd3.take(50))
print('\n\n')
for item in results:
  print('Magnitude= ',item[0],' | Score= ',item[1], ' | Text= ',item[2],'\n')
 
