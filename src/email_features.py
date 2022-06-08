from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from win32com.client import Dispatch
import pandas
import twitter_features
from os import getcwd


currentDirectory = getcwd() + "/" # the bracket makes it easier to concatenate paths
graphImagePath = "output/graph.jpg"
workbookPath = "output/workbook.xlsx" # path to Excel file

# correspondent data
correspondent = "notification0448@gmail.com"
emailPassword = "165621052022"
smtpServer = "smtp.gmail.com"
smtpPort = 587


def createChart(numberOfTweetsList: list, standardAlgorithm: bool) -> None:
	"""
	Creates a chart in Sheet1 of output/workbook.xlsx with the number of tweets over the date.

	Arguments:
		numberOfTweetsList: list of number of tweets for 31 days, the last day being the current day
		standardAlgorithm: boolean indicating whether the standard algorithm is used
	"""
	# create table
	dates = pandas.date_range(end=twitter_features.formatDate(twitter_features.getToday()), periods=31) if standardAlgorithm else pandas.date_range(end=twitter_features.formatDate(twitter_features.getToday()), periods=31, freq='7D') # previous dates that were checked
	dataframe = pandas.DataFrame({ 'Date': dates, 'Tweets': numberOfTweetsList })
	dataframe['Date'] = dataframe['Date'].dt.strftime('%m/%d')
	writer = pandas.ExcelWriter(workbookPath, engine='xlsxwriter') # engine acts a module
	dataframe.to_excel(writer, sheet_name='Sheet1', index=False) # no index; no row and column headers

	# create chart
	workbook = writer.book
	chart = workbook.add_chart({'type': 'line'})
	dateSpan = 'Sheet1!$A$2:$A$32'
	numberOfTweetsSpan = 'Sheet1!$B$2:$B$32'
	chart.add_series({ 'categories': dateSpan, 'values': numberOfTweetsSpan })
	chart.set_x_axis({ 'name': 'Date', 'major_gridlines': { 'visible': False } })
	chart.set_y_axis({ 'name': 'Number of Tweets', 'major_gridlines': { 'visible': True } })
	chart.set_legend({ 'position': 'none' })
	sheet = writer.sheets['Sheet1']
	sheet.insert_chart('D2', chart, { 'x_scale': 1.5, 'y_scale': 1.5 })
	writer.save()


def exportExcelChart(workbookPath: str) -> None:
	"""Exports the only graph in the workbook - Excel file - (with one sheet only) as an image to output folder as graph.jpg."""
	excel = Dispatch("Excel.Application")
	workbook = excel.Workbooks.Open(currentDirectory + workbookPath) # it requires full path
	sheet = workbook.Sheets(1)
	chart = sheet.ChartObjects().Item(1)
	chart.Chart.Export(currentDirectory + graphImagePath)
	workbook.Close()


def sendEmail(recipient: str, subject: str, text: str, imagePath: str) -> None:
	"""
	Sends specified email to recipient from notification0448@gmail.com.

	Arguments:
		recipient: email address of the recipient
		subject: subject of the email
		text: main body of the email
		image: path to the image to be attached to the email
	"""
	# login to email server
	server = smtplib.SMTP(smtpServer, smtpPort) 
	server.starttls()
	server.login(correspondent, emailPassword)

	# create email message
	message = MIMEMultipart('related')
	message['From'] = correspondent
	message['To'] = recipient
	message['Subject'] = subject

	message.attach(MIMEText(f'''
		<h1>{text}</h1>
		<img src="cid:image1">
	''', 'html'))
	with open(imagePath, 'rb') as image:
		messageImage = MIMEImage(image.read())
		messageImage.add_header('Content-ID', '<image1>')
		message.attach(messageImage)

	server.sendmail(correspondent, recipient, message.as_string())
	server.quit()


def sendNotification(recipient: str, hashtag: str, standardAlgorithm: bool, percentile: int, numberOfTweetsList: list) -> None:
	"""Sends email to recipient with statistics depending on the preferred algorithm."""
	subject = f'#{hashtag.capitalize()} is {"" if percentile >= 90 else "not"} trending today'
	createChart(numberOfTweetsList, standardAlgorithm)
	exportExcelChart(workbookPath)
	text = f"Today's percentile is {percentile}% and with {numberOfTweetsList[-1]} tweets."
	sendEmail(recipient, subject, text, graphImagePath)
