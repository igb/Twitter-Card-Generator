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
		"""Extract URLs and Titles of resources from the RSS feed"""
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
					titleData=titleVal[0].data
				extractedLinks.append((linkData, titleData))
		return extractedLinks


	def generateSummaryCardFromDocument(self, document, title):
		

		summary = "\n\n<!-- start of Twitter Summary Card -->\n"
		summary += '<meta name="twitter:card" content="summary">\n'
		summary += '<meta name="twitter:title" content="' + title + '">\n'
		summary += '<meta name="twitter:description" content="' + self.summarize(document,title) + '">\n'
		summary += '<meta name="twitter:site" content="@' + self.twitterHandle + '">\n'
		summary += '<meta name="twitter:creator" content="@' + self.twitterHandle + '">\n'
		summary += "<!-- end of Twitter Summary Card -->\n\n"
		return summary

		
	def getDocument(self, documentUrl):
		docName=documentUrl.rsplit('/', 1)[1]
		req = Request(documentUrl)
		res = urllib2.urlopen(req)
		document=res.read()
		document=unicode(document, errors='replace') 
		return (document, docName)

	def summarize(self, document, title):

		bodyIndex=document.find("<body>")
		closeBodyIndex=document.find("</body>")

		s = MLStripper()
		s.feed(document[bodyIndex:(closeBodyIndex + 7)])
	        snippet=s.get_data()
		snippet=snippet.strip()
		
		#if the title is repeated at the start of the document (as a H1, etc,) strip it out...
		if (snippet.find(title)==0):
			snippet=snippet[len(title):].strip()
		
		#if the snippet is naturally less then 200, leace it alone, otherwise make the last three characters '...'
		if (len(snippet) <= 200):
			return self.sanitize(snippet)
		else:
			snippet=snippet[:197] + "..."
			return self.sanitize(snippet)


	
		
		
	
	def insertSummaryCard(self, document, summaryCard):
		insertionPoint = document.index("<head>") + 6
		return document[:insertionPoint] + summaryCard + document[insertionPoint:]


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

	feedUrl=sys.argv[2]

	outputDir=sys.argv[3]

	cardGenerator =  TwitterSummaryCardGenerator(twitterHandle)
	
	docs=cardGenerator.generateFromRssFeed(feedUrl)
	for doc in docs:
		
		text_file = open(outputDir + "/"  + doc[1], "w")
		text_file.write(doc[0].encode('utf8'))
		text_file.close()

if  __name__ =='__main__':main()	





