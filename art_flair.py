import praw
import time


def parse_new(r, sub):
	#rightnow = time.time()
	subreddit = r.get_subreddit(sub)
	results = []
	
	for submission in subreddit.get_new(limit=None):
		submission_age_in_minutes = (rightnow - submission.created_utc)/60
		
		#if post age > 30 minutes, return all previous results
		if submission_age_in_minutes > 600: #TODO: change this to 30 for 30 minutes
			return results
		
		#if post age is < 30 minutes, add it to results[]
		else:
			results.append(submission)
			
			
def genlog(data):
	f = open(logfile, 'a')
	datetime =  str(time.strftime("%Y/%m/%d")) + " " + str(time.strftime("%H:%M:%S"))
	f.write(datetime + ": " + str(data) + "\n")
	f.close()
	print datetime + ": " + str(data)



### MAIN ############################################################################################################

r = praw.Reddit("/r/naruto art flair by /u/Pandemic21")

username = 'BOT_USERNAME_HERE'
password = 'PASSWORD_HERE'
#r.login(username, password, disable_warning=True) #TODO: uncomment this

title_exceptions = ["BY ", "AUTHOR", "ARTIST", "SOURCE", "OC", "CREDIT"]
domain_exceptions = ["DEVIANTART.COM", "PIXIV.NET", "ARTSTATION.COM"]
do_not_reply = False

logfile = ".\\art_flair.log"
comment_text = """
Hi, if you have you have already given credit to the artist of your fanart submission, please ignore this comment and keep up the good work!\n\n
If **not**, please try to find the original artist using both of the following tools:\n\n
*saucenao.com  \n
*[Google Images](https://images.google.com/)\n\n
Please always try to credit the original artist and link back to them either in the title and link of your post or in the comments. Thank you!
------------------------------------
^(*I am a bot, and this action was performed automatically. Please contact the moderators if you have any questions or concerns.*)
"""

while 1:
	rightnow = time.time()
	results = parse_new(r, "naruto")
	
	#if there is at least 1 post whose age is less than half an hour
	if not results:
		genlog("results[] is empty")
	else:
		genlog("results[] is NOT empty")

		for result in results:
			#make sure it has a link flair
			if not result.link_flair_text:
				genlog("> Skipping, post not flaired: " + result.title + ", " + result.permalink)
			else:
				genlog("> " + result.title + ", " + result.permalink)
				genlog(">> Flair = " + result.link_flair_text.upper())
				
				if result.link_flair_text == "Art":
					
					#check for title exceptions
					for exception in title_exceptions:
						if exception in result.title.upper():
							do_not_reply = True
							genlog(">>> " + exception + " found in " + result.title.upper())
							break
						else:
							genlog(">>> " + exception + " not found")
					
					#check for domain exceptions
					if not do_not_reply:
						for exception in domain_exceptions:
							if exception in result.domain.upper():
								do_not_reply = True
								genlog(">>> " + exception + " found in " + result.domain.upper())
								break
							else:
								genlog(">>> " + exception + " not found")
						
					#check if bot has already replied
					if not do_not_reply:
						for c in result.comments:
							if str(c.author) == username:
								genlog(">>> Already replied, breaking...")
								do_not_reply = True
								break
							else:
								genlog(">>> " + str(c.author) + " isn't me, continuing...")
						
					#if we should reply...
					if not do_not_reply:
						try: 
							#result.add_comment(comment_text) #TODO: uncomment this
							genlog(">>>> Submitted comment")
						except:
							genlog(">>>> I should've added a comment, but I didn't; sorry, there was an error.")
						
					else:
						genlog(">>>> do_not_reply flag is set, skipping")
					
					do_not_reply = False
					
		#sleep for 1 minute
		genlog("Parsed, sleeping...")
		time.sleep(60)
