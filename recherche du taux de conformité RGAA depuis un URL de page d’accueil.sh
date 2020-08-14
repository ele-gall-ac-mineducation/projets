# recherche du taux d’accessibilité depuis un URL de page d’accueil
xidel -s $(xidel -s https://www.monparcourshandicap.gouv.fr/ -f //a -e 'document-uri(.)' -e '//*[starts-with(local-name(), "h")][2 = string-length(local-name())][starts-with(.,"Déclaration")][contains(.,"accessibilité")][not(starts-with(.//*,"Déclaration"))]' | egrep -B1 'Déclaration d.accessibilité' | egrep -v 'Déclaration d.accessibilité') -e '//*[contains(normalize-space(./text()),"des critères RGAA")][contains(normalize-space(./text()),"sont respectés")][not(contains(normalize-space(.//*/text()),"des critères RGAA"))][not(contains(normalize-space(.//*/text()),"respectés"))]'
# renvoie :
# « 100 % des critères RGAA (Version 4) sont respectés. »

