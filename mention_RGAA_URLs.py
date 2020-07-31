#!/usr/bin/env python3
from selenium import webdriver
import time

browser = webdriver.Firefox()

with open('liste_URL.txt') as f:
	lignes = [i.strip() for i in f.readlines()]

def nocomments(item):
	return item[0] != '#'

iterateur = filter(nocomments, lignes)

URLs = list(iterateur)

logfile = open('log.txt', 'w')
logfile.write( 'START' + "\n" )

for url in URLs:
	try:
		browser.get('https://' + url +"\n")
		logfile.write( url + "\n" )
		time.sleep(1)
		logfile.write( browser.current_url + "\n" )

		body = browser.find_element_by_xpath('//body')

		mentions_100 = browser.find_elements_by_xpath(
			"//*[contains(.,'Accessibilité')][contains(.,'totalement conforme')]" # tous les éléments contenant la mention légalement imposée
			+"[not(.//*[contains(.,'Accessibilité')][contains(.,'totalement conforme')])]" # sans enfant la contenant
		) # -> les nœuds les plus profonds contenant la mention, et pas leur ancêtres
		mentions_50 = browser.find_elements_by_xpath(
			"//*[contains(.,'Accessibilité')][contains(.,'partiellement conforme')]" # tous les éléments contenant la mention légalement imposée
			+"[not(.//*[contains(.,'Accessibilité')][contains(.,'partiellement conforme')])]" # sans enfant la contenant
		) # -> les nœuds les plus profonds contenant la mention, et pas leur ancêtres
		mentions_00 = browser.find_elements_by_xpath(
			"//*[contains(.,'Accessibilité')][contains(.,'non conforme')]" # tous les éléments contenant la mention légalement imposée
			+"[not(.//*[contains(.,'Accessibilité')][contains(.,'non conforme')])]" # sans enfant la contenant
		) # -> les nœuds les plus profonds contenant la mention, et pas leur ancêtres

		mentions = mentions_00 + mentions_50+ mentions_100

		# ~ logfile.write(mentions + "\n" )
		logfile.write(str(len(mentions)) + "\n" )

		if (0 < len(mentions)) :
			time.sleep(2)
			for mention in mentions:
				# ~ logfile.write(mention + "\n" )
				# ~ logfile.write('tag='+mention.tag_name + "\n" )
				# ~ logfile.write(round(mention.rect['y']) + "\n" )
				browser.execute_script("window.scrollTo(0,0)")
				browser.execute_script("window.scrollTo(0," + str( round(mention.rect['y']) -10 ) + ")")
				browser.execute_script("arguments[0].setAttribute('style','outline: 5px ridge red ; outline-offset: 3px ; z-index: 999999 ; ');", mention);
			time.sleep(2)
			fichier = url.replace('/','·') + '_screenshot.png'
			browser.get_screenshot_as_file(fichier)
			logfile.write(fichier + "\n" )
			if (0 < len(mentions_00)) :
				logfile.write('mention : non conforme' + "\n" )
			if (0 < len(mentions_50)) :
				logfile.write('mention : partiellement conforme' + "\n" )
			if (0 < len(mentions_100)) :
				logfile.write('mention : totalement conforme' + "\n" )
		else:
			logfile.write('pas de mention RGAA' + "\n" )
		time.sleep(1)
	except:
		logfile.write('erreur' + "\n" )
	finally:
		logfile.write( "\n" );

browser.quit()

logfile.write( 'FINISH' + "\n" )

logfile.close()