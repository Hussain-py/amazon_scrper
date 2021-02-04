from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
from bs4 import BeautifulSoup
import requests
# Create your views here.

class amazon(APIView):
    def get(self,request):
        name = request.query_params.get("Name")
        records = []
        def get_url(search_term):
            """Generate a url from search term"""
            # template = "https://www.amazon.com/s?k={}&crid=Z2EH4B071EU6&sprefix=ul%2Caps%2C419&ref=nb_sb_ss_ts-a-p_2_2"
            # template = "https://www.amazon.in/s?k={}&crid=13QL756WSFKPH&sprefix=led+%2Caps%2C318&ref=nb_sb_ss_ts-a-p_1_4"
            # template = "https://www.amazon.in/s?k={}&rh=n%3A1389401031&ref=nb_sb_nosss"
            # template = "https://www.amazon.com/s?k={}&crid=Z2EH4B071EU6&sprefix=ul%2Caps%2C419&ref=nb_sb_ss_ts-a-p_2_2"
            # template = "https://www.amazon.in/s?k={}&rh=n%3A1389401031&ref=nb_sb_nosss"
            template = "https://www.amazon.in/s?k={}"
            # search_term = search_term.replace(' ', '+')
            search_term = search_term

            # add term query to url
            url = template.format(search_term)

            # add page query placeholder
            # url += '&page{}'
            return url

        def extract_record(item):
            """Extract and return data from a single record"""

            # description and url
            try:
                atag = item.h2.a
                url = "https://www.amazon.in/" + atag.get('href')
                # print(url)
            except:
                url = " "
            try:
                description = atag.text.strip()
            except:
                description = " "
            try:
                # price
                price_parent = item.find('span', 'a-price"')
                price = item.find('span', 'a-offscreen').text
            except AttributeError:
                return

            try:
                # rank and rating
                rating = item.i.text
                review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
            except:
                rating = ' '
                review_count = ' '


            result= {
                'ProductTypeId': 1,
                'ProductName': description,
                'price': price,
                'Rating': rating,
                'ReviewCount': review_count,
                'Url': url
            }

            # result = (description, price, rating, review_count, url)
            # print(result)
            return result

        def main(search_term):
            """Run main program routine"""
            url = get_url(search_term)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

            r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})
            for item in results:
                record = extract_record(item)
                if record:
                    records.append(record)
            # print(json.dumps(records))

        main(name)
        # y = json.dumps(result)
        # return  Response(y)
        return  Response(records)
    def post(self):
        pass


class amflip(APIView):
    def get(self,request):
        name = request.query_params.get("Name")
        records = []
        def get_url(search_term):
            """Generate a url from search term"""
            template = "https://www.amazon.in/s?k={}"
            # search_term = search_term.replace(' ', '+')
            search_term = search_term

            # add term query to url
            url = template.format(search_term)

            return url

        def extract_record(item):
            """Extract and return data from a single record"""

            # description and url
            try:
                atag = item.h2.a
                url = "https://www.amazon.in/" + atag.get('href')
                print(url)
            except:
                url = " "

            try:
                description = atag.text.strip()
            except:
                description = " "

            try:
                # price
                price_parent = item.find('span', 'a-price"')
                price = item.find('span', 'a-offscreen').text
            except AttributeError:
                return

            try:
                # rank and rating
                rating = item.i.text
                review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
            except:
                rating = ' '
                review_count = ' '


            result= {
                'ProductTypeId': 1,
                'ProductName': description,
                'price': price,
                'Rating': rating,
                'ReviewCount': review_count,
                'Url': url
            }

            # result = (description, price, rating, review_count, url)
            print(result)
            return result

        def main(search_term):
            """Run main program routine"""
            url = get_url(search_term)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

            r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})
            for item in results:
                record = extract_record(item)
                if record:
                    records.append(record)
        main(name)


        # name = request.query_params.get("Name")

        search_term = name
        # template = "https://www.flipkart.com/search?q={}"
        template = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        search = search_term.replace(' ', '+')
        url = template.format(search)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # records = []
        for a in soup.findAll('a', href=True, attrs={'class': '_1fQZEK'}):
            try:
                atag = a.get('href')
                url = "https://www.flipkart.com" + atag
            except:
                url = " "
            try:
                proName = a.find('div', attrs={'class': '_4rR01T'}).get_text()
            except:
                proName = " "
            try:
                price = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).get_text()
            except:
                price = " "
            try:
                rating = a.find('div', attrs={'class': '_3LWZlK'}).get_text()
            except:
                rating = " "

            # result = (name, price, rating, url)
            result = {
                'ProductTypeId': 2,
                'ProductName': proName,
                'Price': price,
                'Rating': rating,
                'Url': url
                }
            # print(result)
            records.append(result)
        # if records == []:
        for item in soup.findAll('div', attrs={'class': '_4ddWXP'}):
            try:
                atag = item.find('a', href=True, attrs={'class': '_2rpwqI'}).get('href')
                url = 'https://www.flipkart.com' + atag
            except:
                url = ""
            try:
                des = item.find('a', attrs={'class': 's1Q9rs'}).get_text()
            except:
                des = " "
            try:
                size = item.find('div', attrs={'class': '_3Djpdu'}).get_text()
            except:
                size = " "
            try:
                price = item.find('div', attrs={'class': '_30jeq3'}).get_text()
            except:
                price = " "
            try:
            # rank and rating
                rating = item.find('div', attrs={'class': '_3LWZlK'}).get_text()
            except:
                rating = ' '
                print(rating)
                # result = (name, price, rating, url)
            result = {
                        'ProductTypeId': 2,
                        'ProductName': des,
                        'Size': size,
                        'Price': price,
                        'Rating': rating,
                        'Url': url
                    }
            # print(result)
            records.append(result)

        for item in soup.findAll('div', attrs={'class': '_1xHGtK _373qXS'}):
            try:
                atag = item.find('a', href=True, attrs={'class': '_3bPFwb'}).get('href')
                url = 'https://www.flipkart.com' + atag
            except:
                url = ""
            # try:
            #     producttype =item.find('a', attrs={'class': 'IRpwTa _2-ICcC'}).get_text()
            # except:
            #     producttype = ""
            try:
                name = item.find('div', attrs={'class': '_2WkVRV'}).get_text()
            except:
                name = " "
            try:
                price = item.find('div', attrs={'class': '_30jeq3'}).get_text()
            except:
                price = " "
            # try:
            #     # rank and rating
            #     rating = item.find('div', attrs={'class': '_3LWZlK'}).get_text()
            # except:
            #     rating = ' '
            #     print(rating)

                # result = (name, price, rating, url)
            result = {
                    'ProductTypeId': 2,
                    'ProductName': name,
                    'Price': price,
                    'Url': url
                }
            records.append(result)
        return Response(records)

    def post(self):
        pass


class flipkart(APIView):
    def get(self,request):
        name = request.query_params.get("Name")

        search_term = name
        # template = "https://www.flipkart.com/search?q={}"
        template = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        search = search_term.replace(' ', '+')
        url = template.format(search)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup)

        records = []
        for a in soup.findAll('a', href=True, attrs={'class': '_1fQZEK'}):
            atag = a.get('href')

            name = a.find('div', attrs={'class': '_4rR01T'}).get_text()
            price = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).get_text()
            rating = a.find('div', attrs={'class': '_3LWZlK'}).get_text()
            url = "https://www.flipkart.com" + atag
            # result = (name, price, rating, url)
            result = {
                'ProductTypeId': 2,
                'ProductName': name,
                'Price': price,
                'Rating': rating,
                'Url': url
            }
            print(result)
            records.append(result)
        if records == [] :
            for item in soup.findAll('div', attrs={'class': '_4ddWXP'}):
                try:
                    atag = item.find('a', href=True, attrs={'class': '_2rpwqI'}).get('href')
                    url = 'https://www.flipkart.com' + atag
                except:
                    url = ""
                try:
                    name = item.find('a', attrs={'class': 's1Q9rs'}).get_text()
                except:
                    name = " "
                try:
                    size = item.find('div', attrs={'class': '_3Djpdu'}).get_text()
                except:
                    size = " "
                try:
                    price = item.find('div', attrs={'class': '_30jeq3'}).get_text()
                except:
                    price = " "
                try:
                    # rank and rating
                    rating = item.find('div', attrs={'class': '_3LWZlK'}).get_text()
                except:
                    rating = ' '
                    print(rating)

                # result = (name, price, rating, url)
                result = {
                    'ProductTypeId': 2,
                    'ProductName': name,
                    'Size': size,
                    'Price': price,
                    'Rating': rating,
                    'Url': url
                }
                print(result)
                records.append(result)
        return Response(records)
    def post(self):
        pass



class newf(APIView):
    def get(self,request):
        name = request.query_params.get("Name")

        search_term = name
        # template = "https://www.flipkart.com/search?q={}"
        template = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        search = search_term.replace(' ', '+')
        url = template.format(search)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        records = []
        for item in soup.findAll('div', attrs={'class': '_1xHGtK _373qXS'}):
            try:
                atag = item.find('a', href=True, attrs={'class': '_3bPFwb'}).get('href')
                url = 'https://www.flipkart.com' + atag
            except:
                url = ""
            # try:
            #     producttype =item.find('a', attrs={'class': 'IRpwTa _2-ICcC'}).get_text()
            # except:
            #     producttype = ""
            try:
                name = item.find('div', attrs={'class': '_2WkVRV'}).get_text()
            except:
                name = " "
            try:
                price = item.find('div', attrs={'class': '_30jeq3'}).get_text()
            except:
                price = " "
            # try:
            #     # rank and rating
            #     rating = item.find('div', attrs={'class': '_3LWZlK'}).get_text()
            # except:
            #     rating = ' '
            #     print(rating)

                # result = (name, price, rating, url)
            result = {
                    'ProductTypeId': 2,
                    'ProductName': name,
                    'Price': price,
                    'Url': url
                }
            records.append(result)
        return Response(records)
    def post(self):
        pass
