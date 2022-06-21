import boto3
import setting
from time import sleep
import csv

# Comprehend client
comp_client = boto3.client('comprehend', region_name='us-east-2',
                           aws_access_key_id=setting.AWSAccessKeyId,
                           aws_secret_access_key=setting.AWSSecretKey)

text_list = []
# read the input file and convert to list, we need to send batch of 25
with open('input.csv') as csvfile:
    textreader = csv.reader(csvfile)
    for row in textreader:
        text_list.append(row[0])

# print(text_list)

# loop through the list and process batch of 25
with open('output.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['input', 'sentiment', 'sentiment_score'])
    for text in text_list[1:]:
        try:
            response = comp_client.batch_detect_sentiment(
                TextList=[text], LanguageCode='en'
            )
            writer.writerow(
                [text,
                 response['ResultList'][0]['Sentiment'],
                 response['ResultList'][0]['SentimentScore']
                 ]
            )
            print(text)
            print(response['ResultList'][0]['Sentiment'])
            print(response['ResultList'][0]['SentimentScore'])
            sleep(5)
        except Exception as e:
            print(e)
            pass
