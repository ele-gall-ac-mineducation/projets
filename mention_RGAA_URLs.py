#!/usr/bin/env python3
# licence ouverte https://www.etalab.gouv.fr/licence-ouverte-open-licence - travail personnel sur temps libre
# vérifie la présence des mentions obligatoires RGAA 4 de la page d’accueil d’un « service de communication au public en ligne » :
# « Accessibilité : non conforme »
# « Accessibilité : partiellement conforme »
# « Accessibilité : totalement conforme »
# aux espaces près (doublées*, insécables, retours à la ligne…)
# * https://www.w3.org/TR/1999/REC-xpath-19991116/#function-normalize-space
# en cas de réussite prend une capture d’écran pour vérification postérieure
# prend en entrée une liste d’URL (sans http… devant), en éliminant les lignes débutant par un #
# pas parfait mais mieux que rien… (notamment des erreurs qui bouclent parfois) :
# merci à Bastien et Nicolas (de me persuader de publier un code dans un tel état… même s’il se bonifie ;)
# contributions de pythonistes bienvenues (n’en suis pas)
# v1.0 : prise en compte exacte de la mention.
# TODO Cas des mentions multiples incohérentes non traité cf www.numerique.gouv.fr/publications/rgaa-accessibilite/obligations ;)
# TODO Cas des URLs fausses à catcher (non loguées actuellement)
# v0.9 : version initiale
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
	logfile.write( url + "\n" )
	try:
		browser.get('http://' + url +"\n")
		time.sleep(1)
		logfile.write( browser.current_url + "\n" )

		body = browser.find_element_by_xpath('//body')

		# note : translate(./text(),' ',' ') est en fait translate(./text(),'&nbsp;',' ') = remplacement des espaces insécables (indistinguables)
		mentions_100 = browser.find_elements_by_xpath(
			#  tous les éléments (×3)
			"//*"
			# contenant la mention légalement imposée
			+"[         contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : totalement conforme')]"
			# sans enfant la contenant
			+"[not(.//*[contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : totalement conforme')])]"
		) # -> les nœuds les plus profonds contenant la mention, et pas leur ancêtres
		mentions_50 = browser.find_elements_by_xpath(
			"//*"
			+"[         contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : partiellement conforme')]"
			+"[not(.//*[contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : partiellement conforme')])]"
		)
		mentions_00 = browser.find_elements_by_xpath(
			"//*"
			+"[         contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : non conforme')]"
			+"[not(.//*[contains(normalize-space(translate(translate(translate(./text(),' ',' '),'\r',' '),'\n',' ')),'Accessibilité : non conforme')])]"
		)

		mentions = mentions_00 + mentions_50 + mentions_100

		# ~ logfile.write(mentions + "\n" )
		# ~ logfile.write(str(len(mentions)) + "\n" )

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
			# ~ browser.get_screenshot_as_file(fichier)
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

# ~ browser.quit()

logfile.write( 'FINISH' + "\n" )

logfile.close()
