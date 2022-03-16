 #!/usr/bin/env python
# -*- coding: utf-8 -*-
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
from nltk.corpus import stopwords
import math

from lxml import html  
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep

############################## PARSE REVIEWS FROM AMAZON ############################################
def ParseReviews(asin):
	dola=[]
	 
	for i in range(500): 
		amazon_url  = asin
		print(amazon_url)
		#https://www.amazon.in/OnePlus-Midnight-Black-64GB-memory/product-reviews/B0756ZFXVB/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2
		#amazon_url  = 'http://www.amazon.com/Samsung-Galaxy-J7-Contract-Carrier/product-reviews/'+asin+'/ref=cm_cr_getr_d_paging_btm_+'+j+'?ie=UTF8&reviewerType=all_reviews&pageNumber=+'+j
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
		page = requests.get(amazon_url,headers = headers)
		page_response = page.text
		
		parser = html.fromstring(page_response)
		XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
		XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
		XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
		 
		XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
		XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
		XPATH_PRODUCT_PRICE  = '//span[@id="priceblock_ourprice"]/text()'
		
		raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
		product_price = ''.join(raw_product_price).replace(',','')

		raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
		product_name = ''.join(raw_product_name).strip()
		total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
		reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
		if not reviews:
			reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
		ratings_dict = {}
		reviews_list = []
		dola_1=[]
		list_1=[]
		review_dict1 = {
                        'review_text':'neutral',
			 }
		list_1.append(review_dict1)

		data_1 = {
                        'reviews':list_1
			}
		dola_1.append(data_1)
		if not reviews:
			return dola_1

		#grabing the rating  section in product page
		for ratings in total_ratings:
			extracted_rating = ratings.xpath('./td//a//text()')
			if extracted_rating:
				rating_key = extracted_rating[0] 
				raw_raing_value = extracted_rating[1]
				rating_value = raw_raing_value
				if rating_key:
					ratings_dict.update({rating_key:rating_value})
		#Parsing individual reviews
		
		for review in reviews:
			XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
			XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
			XPATH_REVIEW_POSTED_DATE = './/a[contains(@href,"/profile/")]/parent::span/following-sibling::span/text()'
			XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
			XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
			XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
			XPATH_AUTHOR  = './/a[contains(@href,"/profile/")]/parent::span//text()'
			XPATH_REVIEW_TEXT_3  = './/div[contains(@id,"dpReviews")]/div/text()'
			raw_review_author = review.xpath(XPATH_AUTHOR)
			raw_review_rating = review.xpath(XPATH_RATING)
			raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
			raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
			raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
			raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
			raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

			author = ' '.join(' '.join(raw_review_author).split()).strip('By')

			#cleaning data
			review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
			review_header = ' '.join(' '.join(raw_review_header).split())
			 
			review_text = ' '.join(' '.join(raw_review_text1).split())
			#print(review_text)
			#grabbing hidden comments if present
			if raw_review_text2:
				json_loaded_review_data = json.loads(raw_review_text2[0])
				json_loaded_review_data_text = json_loaded_review_data['rest']
				cleaned_json_loaded_review_data_text = re.sub('<.*?>','',json_loaded_review_data_text)
				full_review_text = review_text+cleaned_json_loaded_review_data_text
			else:
				full_review_text = review_text
			if not raw_review_text1:
				full_review_text = ' '.join(' '.join(raw_review_text3).split())

			raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
			review_comments = ''.join(raw_review_comments)
			review_comments = re.sub('[A-Za-z]','',review_comments).strip()
			review_dict = {
								 
								'review_text':full_review_text,
								 

							}
			reviews_list.append(review_dict)

		data = {
					 
					'reviews':reviews_list
					 
				}
		dola.append(data)
		data={}
		reviews_list=[]
		review_dict={}
		return dola
	return {"error":"failed to process the page","asin":asin} 

############################################################################	 

############### ENTER URL AND EXTRACT DATA ##################################################


def ReadAsin():
	#Add your own ASINs here 
	URL = input("ENTER THE URL........ ")
	AsinList = [URL]
	data=URL.split('dp')
	 
	main_url1=(str)(data[0])
	main_url2=(str)(data[1][1:11])
	 
        
	for asin in AsinList:
		print ("Downloading and processing page "+asin)
		extracted_data = []
		for m in range(1,48): 
			j=(str)(m)
			
			asin=main_url1+'product-reviews/'+main_url2+'/ref=cm_cr_arp_d_paging_btm_'+j+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+j
			
            
			extracted_data.append(ParseReviews(asin))
		file_name='data_amazon_in_'+main_url2+'.json'
		f=open(file_name,'w')
		json.dump(extracted_data,f,indent=4)
		sleep(5)
		return file_name


#########################################################################



####################### POLARITY DECIDER #################################




def polarity(file_name):
        stop_words=set(stopwords.words("english"))

        ps=PorterStemmer()
 
        final_score=0
        eight_above=0
        six_to_eight=0
        four_to_six=0
        two_to_four=0
        less_than_two=0


        rating=0

                               
         
        sentences=[]
        with open(file_name) as json_file:  
            data = json.load(json_file)
            for item in data:
                #print(item)
                for item1 in item:
                    #print(item1)
                    list=item1.get("reviews")
                     
                    for item2 in list:
                        review_text=item2.get("review_text")
                        #print(review_text)
                        ####### REMOVING STOP WORDS ##################
                        token_text=word_tokenize(review_text)
                        #print(token_text)
                        
                        filtered_review=[w for w in token_text if not w in stop_words]
                          
                        sentences.append(filtered_review)
                        #############################################

         
                
        #print(sentences)
        sid = SentimentIntensityAnalyzer()
        count=0
        for sentence in sentences:
              count=count+1
              ####### STEMMING WORDS ##################
              ss=''
              for w in sentence:
                  w.encode('ascii','ignore')
                  ss+=ps.stem((w))+' '
                      
              #########################################   
              #print(ss)
              
              ####### GETTING POLARITY ################ 
             
              score=sid.polarity_scores(ss).get('compound')
              ##########################################

              
              ###### CALCULATING SCORES ################
              
              score=(1-(1-(score))/2)*10
              if score>=8:
                  eight_above=eight_above+1
              elif score>=6 and score<8:
                  six_to_eight=six_to_eight+1
              elif score>=4 and score<6:
                  four_to_six=four_to_six+1
              elif score>=2 and score<4:
                   two_to_four=two_to_four+1
              elif score<2:
                    less_than_two=less_than_two+1


               
              print(score)
              final_score+=score
              
        #################################################
         
        print('FINAl SCORE '+(str)(math.ceil(final_score/count)))
        print()
        print('SOME STATS')
        print('TOTAL COMMENTS          '+(str)(count))
        print('Comments Greater than 8 '+(str)(eight_above))
        print('Comments between 6-8    '+(str)(six_to_eight))
        print('Comments between 4-6    '+(str)(four_to_six))
        print('Comments between 2-4    '+(str)(two_to_four))
        print('Comments between 0-2    '+(str)(less_than_two))
	
if __name__ == '__main__':
        file_name=ReadAsin()
        #file_name='data_amazon_in_Moto-Plus-.json'
        polarity(file_name)
