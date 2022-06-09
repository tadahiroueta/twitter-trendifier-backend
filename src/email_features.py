import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getcwd
from matplotlib import pyplot
import date_features


graphImagePath = "output/graph.jpg"

# correspondent data
correspondent = "twittertrendification@outlook.com"
emailPassword = "5as1dff651adfs51afsd"
smtpServer = "smtp-mail.outlook.com"
smtpPort = 587


def createChart(numberOfTweetsList: list, standardAlgorithm: bool) -> None:
	"""
	Creates and stores a bar chart into the graph image path.

	Arguments:
		numberOfTweetsList: list of number of tweets for 31 days, the last day being the current day
		standardAlgorithm: boolean indicating whether the standard algorithm is used
	"""
	# get x axis
	dates = date_features.getContinuosDates() if standardAlgorithm else date_features.getWeeklyDates()

	# generate graph
	_, axes = pyplot.subplots()
	axes.bar(dates, numberOfTweetsList)

	# rotate the dates to vertical position
	for tick in axes.get_xticklabels():
		tick.set_rotation(90)

	axes.set_ylabel('Number of Tweets')
	axes.set_xlabel('Date')

	# save graph
	pyplot.savefig(graphImagePath)


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
	text = f"Today's percentile is {percentile}% and with {numberOfTweetsList[-1]} tweets."
	sendEmail(recipient, subject, text, graphImagePath)
