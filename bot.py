from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import csv

'''
This program automates liking, commenting and following users on Instagram.

@author: Jonathan Shreckengost (jonathanshrek@gmail.com)
'''

class InstaBot():
    
    def __init__(self, path, username, password, hashlist):
        self.chromedriver_path = path
        self.username = username
        self.password = password
        self.hashtagList = hashlist
        
    def bot(self):
        # Creates a webdriver to access and execute content
        webdrive = webdriver.Chrome(executable_path=self.chromedriver_path)
        sleep(2)
        # Opens instagram
        webdrive.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3)
        
        # Finds username box
        username = webdrive.find_element_by_name('username')
        # Inputs given username
        username.send_keys(self.username)
        # Finds password box
        password = webdrive.find_element_by_name('password')
        # Inputs given password
        password.send_keys(self.password)
        
        # Finds the login button
        button_login = webdrive.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
        # Activates the login button
        button_login.click()
        sleep(3)
        
        # Gets rid of the allow notifications pop up
        # If you do not get this comment out these two lines
        notnow = webdrive.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
        notnow.click() 
        
        # Creates a list of seen users
        prev_user_list = []
        
        # Creates a new list that allows us to track who we follow
        new_followed = []
        # Allows us to increment through our list of defined hashtags
        tag = -1
        # Tracks the number of people we follow
        followed = 0
        # Tracks the number of likes we give
        likes = 0
        # Tracks the number of comments we give
        comments = 0
        
        # Loops each hashtag in our defined list
        for hashtag in self.hashtagList:
            # Increments to the next tag in the list
            tag += 1
            # Opens the webpage associated with the given hashtag
            webdrive.get('https://www.instagram.com/explore/tags/'+ self.hashtagList[tag] + '/')
            sleep(5)
            # Opens the first picture shown for the given hashtag
            first_thumbnail = webdrive.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            first_thumbnail.click()
            sleep(randint(1,2))
             
            try:
                # Loops through each photo in the given hashtag
                for x in range(1,200):
                    # Gets the username
                    username = webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
                    
                    # If username hasn't been seen before
                    if username not in prev_user_list:
                        
                        # If we already follow, do not unfollow
                        if webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                            
                            # Clicks follow button
                            webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                            
                            # Appends the username to the new_followed list
                            new_followed.append(username)
                            # To track how many people we follow
                            followed += 1
        
                            # Likes the picture
                            button_like = webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                            button_like.click()
                            # To track how many likes we give
                            likes += 1
                            sleep(randint(18,25))
        
                            # Gives out comments
                            # Allows us to randomize who we give comments out to
                            comm_prob = randint(1,10)
                            
                            # If comm_prob is greater than 7 we will leave a comment
                            # At this rate each photo has a 40% of receiving a comment
                            if comm_prob >= 7:
                                # Tracks how many comments we give out
                                comments += 1
                                # Clicks the comment button
                                webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button').click()
                                # Finds the comment area
                                comment_box = webdrive.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
                                
                                # Determines which comment to give
                                if (comm_prob == 7):
                                    comment_box.send_keys('Really cool!')
                                    sleep(1)
                                elif (comm_prob == 8):
                                    comment_box.send_keys('Looks great!')
                                    sleep(1)
                                elif comm_prob == 9:
                                    comment_box.send_keys('Nice')
                                    sleep(1)
                                elif comm_prob == 10:
                                    comment_box.send_keys('So cool!')
                                    sleep(1)
                                    
                                # Enter to post comment
                                comment_box.send_keys(Keys.ENTER)
                                sleep(randint(22,28))
        
                        # Next picture
                        webdrive.find_element_by_link_text('Next').click()
                        sleep(randint(12,61))
                    else:
                        # Next picture
                        webdrive.find_element_by_link_text('Next').click()
                        sleep(randint(3,11))
            except:
                continue
        
        # Appends new followed accounts to previous users list
        for n in range(0,len(new_followed)):
            prev_user_list.append(new_followed[n])
            
        # Writes new follows, number of comments, and number of likes to a csv
        timestr = strftime("%Y/%m/%d")
        with open('Instabot_Activity.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["DATE", "NUMBER FOLLOWED", "NUMBER COMMENTED", "NUMBER LIKED"])
            
            rows = timestr, followed, comments, likes
            csv_writer.writerow(rows)
            
            f.close()
            
        #FIXME
        # Not writing to the .csv properly
        updated_user_df = prev_user_list
        with open('Instabot_Followed.csv', 'w') as i:
            csv_writer = csv.writer(i)
            csv_writer.writerow(["NAMES"])
            
            row = zip(updated_user_df)
            for row in rows:
                csv_writer.writerow(row)
                
            i.close()


def main():
    # Set your path to your driver (chromedriver, etc)
    path = '/usr/lib/chromium/chromedriver'
    # Instagram username
    username = "godhatesfigz"
    # Instagram password
    password = "123113"
    # List of hashtags to be searched
    hashtag_list = ["metal", "guitar", "computers", "pcmasterrace"]
    
    # Creates a variable with the ability to access the InstaBot class
    # Passes unique information to the InstaBot class
    bot = InstaBot(path, username, password, hashtag_list)
    
    # Runs the bot() method from the InstaBot class
    bot.bot()
    
    

if __name__ == '__main__':
    main()

