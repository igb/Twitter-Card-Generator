import sys, urllib2, cgi
from MLStripper import MLStripper
from urllib2 import Request
from xml.dom.minidom import parse, parseString


class TwitterSummaryCardGenerator():
	"""docstring for TwitterSummaryCardGenerator"""
	def __init__(self, twitterHandle):
		self.twitterHandle = twitterHandle
		
	def sanitize(self, summary):
	    return cgi.escape(summary, True)

	def extractLinksAndTitlesFromRssFeed(self, feedUrl):
		"""Extract URLs of resources from the RSS feed"""
		extractedLinks=[]
		req = Request(feedUrl)
		res = urllib2.urlopen(req)
		feedom = parseString(res.read())
		channels=feedom.getElementsByTagName("channel")
		for channel in channels:
			items=channel.getElementsByTagName("item")
			for item in items:
				linkData=""
				titleData=""
				links = item.getElementsByTagName("link")				
				for link in links:
					linkVal = link.childNodes
					linkData=linkVal[0].data
				titles = item.getElementsByTagName("title")
				for title in titles:
					titleVal = title.childNodes
					titleData=linkVal[0].data
				extractedLinks.append((titleData, linkData))
		return extractedLinks


	def generateSummaryCardFromDocument(self, document, title):
		summary = ""
		summary += '<meta name="twitter:card" content="summary">\n'
		summary += '<meta name="twitter:title" content="' + title + '">\n'
		summary += '<meta name="twitter:description" content="' + self.summarize(document) + '">\n'
		summary += '<meta name="twitter:creator" content="@' + self.twitterHandle + '">\n'
		return summary

		
	def getDocument(self, documentUrl):
		docName=documentUrl.rsplit('/', 1)[1]
		print docName
		req = Request(documentUrl)
		res = urllib2.urlopen(req)
		document=res.read()
		return (document, docName)

	def summarize(self, document):
		contentStart=0;
		firstParagraphIndex=document.find("<p>")
		if firstParagraphIndex == -1:
			bodyIndex=document.find("<body>")
			contentStart=bodyIndex + 6
		else:
			contentStart=firstParagraphIndex + 3
		s = MLStripper()
		s.feed(document)
		print s.get_data()
	
		snippet=(document[contentStart:])[:200]
		return self.sanitize(snippet)
	
	def insertSummaryCard(self, document, summaryCard):
		insertionPoint = document.index("<head>") + 6
		print summaryCard


	def generateFromRssFeed(self, feedUrl):
		"""Generate HTML documents containing Twitter Summary Cards from an RSS feed containing links to target documents"""
		documentsWithCards=[];
		documentLinksAndTitles=self.extractLinksAndTitlesFromRssFeed(feedUrl)
		for documentLinkAndTitle in documentLinksAndTitles:
			(documentUrl, title)=documentLinkAndTitle
			(document, documentName)=self.getDocument(documentUrl)
			summaryCard=self.generateSummaryCardFromDocument(document, title)
			documentWithCard=self.insertSummaryCard(document, summaryCard)
			documentsWithCards.append((documentWithCard, documentName))
		return documentsWithCards
	


def main():
	
	twitterHandle=sys.argv[1]
	print twitterHandle 
	feedUrl=sys.argv[2]
	print feedUrl
	cardGenerator =  TwitterSummaryCardGenerator(twitterHandle)
	
	cardGenerator.generateFromRssFeed(feedUrl)

if  __name__ =='__main__':main()	





