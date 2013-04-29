import sys, urllib2
from urllib2 import Request
from xml.dom.minidom import parse, parseString



def extractLinksFromRssFeed(feedUrl):
	"""Extract URLs of resources from the RSS feed"""
	extractedLinks=[]
	req = Request(feedUrl)
	res = urllib2.urlopen(req)
	feedom = parseString(res.read())
	channels=feedom.getElementsByTagName("channel")
	for channel in channels:
		items=channel.getElementsByTagName("item")
		for item in items:
			links = item.getElementsByTagName("link")
			for link in links:
				linkVal = link.childNodes
				extractedLinks.append(linkVal[0].data)
	return extractedLinks
		
def getDocument(documentUrl):
	docName=documentUrl.rsplit('/')[1]
	prints docName
	req = Request(documentUrl)
	res = urllib2.urlopen(req)
	document=res.read()
	firstParagraphIndex=document.find("<p>")
	print (document[firstParagraphIndex + 3:])[:200]
	
def generateFromRssFeed(feedUrl):
	"""Generate HTML documents containing Twitter Summary Cards from an RSS feed containing links to target documents"""
	documentsWithCards=[];
	documentUrls=extractLinksFromRssFeed(feedUrl)
	for documentUrl in documentUrls:
		(document, documentName)=getDocument(documentUrl)
		summaryCard=generateSummaryCardFromDocument(document)
		documentWithCard=insertSummaryCard(document)
		documentsWithCards.append((documentWithCard, documentName))
	return documentsWithCards
	
	


def main():
	feedUrl=sys.argv[1]
	generateFromRssFeed(feedUrl)

if  __name__ =='__main__':main()	