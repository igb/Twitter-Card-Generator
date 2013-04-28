def generateFromRssFeed(feedUrl):
	"""Generate HTML documents containing Twitter Summary Cards from an RSS feed containing links to target documents"""
	documentsWithCards=[];
	documentUrls=extractLinksFromRssFeed(feedUrl)
	for documentUrl in documentUrls:
		(document, documentName)=getDocument(documentUrl)
		summaryCard=generateSummaryCardFromDocument(document)
		documentWithCard=insertSummaryCard(document)
		documentsWithCards.append((documentWithCard, documentName)
	return documentsWithCards