# recherche de déclaration d’accessibilité depuis un URL
xidel -s https://www.monparcourshandicap.gouv.fr/ -f //a -e 'document-uri(.)' -e '//*[starts-with(local-name(), "h")][2 = string-length(local-name())][starts-with(.,"Déclaration")][contains(.,"accessibilité")][not(starts-with(.//*,"Déclaration"))]' | egrep -B1 'Déclaration d.accessibilité'
# renvoie :
# https://www.monparcourshandicap.gouv.fr/accessibilite-numerique
#Déclaration d'accessibilité

