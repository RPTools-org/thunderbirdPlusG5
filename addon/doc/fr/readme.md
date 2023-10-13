# Thunderbird+G5 pour Thunderbird >= 115

* Auteurs: Pierre-Louis Renaud (From Thunderbird 78 to 115) & Cyrille Bougot (TB 102), Daniel Poiraud (From TB 78 to 91), Yannick (TB 45 to 60);
* URL: [Accueil des extensions thunderbirdPlus][4] ;
  [Historique des changements][5] ;
  [Contact][6] ;
* Télécharger : [Version stable][1]
* Télécharger : [Dernière version sur RPTools.org][3] ;
* Ccompatibilité NVDA : 2021.1 et ultérieures ;
* [Code Source  sur gitHub][2]


## Introduction
Thunderbird+G5 est une extension pour NVDA qui augmente considérablement l'efficacité et le confort d'utilisation du client de messagerie  Thunderbird 115.

Elle améliore votre productivité en fournissant des commandes qui n'existent pas nativement dans Thunderbird :

* des raccourcis-clavier d'accès direct à l'arborescence des dossiers, à la liste de messages et au volet d'aperçu.
* Une navigation sans détours entre les volets  de la fenêtre principale grâce aux touches Tab et échappe.
* Des raccourcis de consultation et copie des champs de la liste de messages et des entêtes de message sans changement de focus.
* Un accès direct aux pièces jointes.
* Des raccourcis de consultation et d'accès directs aux champs d'adressage de la fenêtre de rédaction.
* Une amélioration considérable de l'utilisation du dialogue de vérification orthographique.
* et bien d'autres choses encore... 

Cette page documente les raccourcis clavier proposés par Thunderbird+G5. 

La plupart de ces raccourcis-clavier sont configurables via le Menu NVDA / Préférences / Gestes de commande / catégorie thunderbirdPlusG5 pour Thunderbird 115

## Navigation dans la fenêtre principale

Note : La touche nommée (touche au dessus de Tab) dans la suite de cette page désigne la touche qui se trouve en-dessous de Echappe, au-dessus de Tab et à gauche du chiffre 1. Son libellé varie en fonction de la langue du clavier.

### Raccourcis généraux
* (touche au-dessus de Tab) : affiche le menu des commandes diverses de l'extension.
* Maj+(touche au-dessus de Tab) : Affiche le menu des options de l'extension.
* F8 pour afficher ou masquer le volet d'aperçu : cette commande est vocalisée par l'extension.
* Control+F1 : affiche la présente page. Pour certains éclaircissements, vous pouvez [visiter la documentation de la version4][7] ;

### Navigation entre les volets de la fenêtre principale
Ces raccourcis concernent l'arborescence des dossiers, la liste de messages et le volet d'aperçu du message.

* control+(touche au-dessus de Tab) : Un appui place le focus dans la liste de messages, deux appuis place le focus dans la liste de messages puis sélectionne le dernier message.
* alt+Début : 1 appui sélectionne le dossier courant dans l'arborescence des dossiers, 2 appuis affiche un menu permettant de choisir le compte de messagerie à atteindre dans l'arborescence 
* Tab : va au volet suivant, sans détour.
* Echappe : revient au volet précédent, sans détour. 
Echappe permet aussi d'alterner entre l'arborescence des dossiers et la liste de messages. 
* Maj+Tab : son comportement natif a été conservé dans cette version.

### Navigation parmi les onglets de la fenêtre principale

* Control+Tab avec ou sans la touche majuscule et control+1 à 9 : L'extension intercepte les changements d'onglet afin d'annoncer leur numéro d'ordre et le nombre total d'onglets.
* Control+la première touche située à gauche de retour-arrière : affiche un menu avec la liste des onglets existants. Pressez Entrée sur un élément de menu pour activer l'onglet correspondant.
* Alt+la première touche située à gauche de retour-arrière : affiche le menu contextuel des onglets.Ce menu est natif de Thunderbird.

Note : Le libellé de la première touche à gauche de retour-arrière varie en fonction de la langue du clavier.

## Liste de messages
Avant d'annoncer une ligne de la liste de messages, l'extension la nettoie pour la rendre plus agréable à écouter ou à lire. Explorez les options du menu Maj+(touche au-dessus de Tab) / Options pour la fenêtre principale pour les ajuster.

Si ce nettoyage ralentit trop la navigation dans la liste sur votre PC, pressez  Maj+(touche au-dessus de Tab) / Désactivations. Vous pourrez le désactiver là.

Remarque : Les colonnes "Non lu" et "Statut de lecture" ne peuvent plus être annoncées par ThunderbirdPlus. utiliser la colonne "Statut" à la place. Le statut "non lu" est annoncé  et le statut "lu" est réduit au silence. Pour supprimer et ajouter des colonnes, placez-vous dans la liste de messages puis pressez Maj+Tab. Utilisez ensuite flèche gauche et droite pour trouver "Choisir les colonnes à afficher".

* Echappe dans la liste de messages : si un filtre est actif, il est désactivé et la liste de messages reste sélectionnée. Sinon, ce raccourci donne le focus à l'arborescence des dossiers.
* NVDA+flèche haut dans la liste de messages :<br>
Un appui : annonce la ligne courante de la liste de messages. Le raccourci NVDA+Tab produit le même résultat mais sans passer par cette extension.<br>
Deux appuis : affiche le détail de la ligne dans une fenêtre de texte qui permet l'analyse de la ligne au clavier.
* Espace, F4 ou Alt+flèche bas : lit une version épurée du message du volet d'aperçu, sans quitter la liste de messages.
* Alt+flèche haut : place le message dans le navigateur virtuel de citations ;
* Windows+flèches bas ou haut : lit la citation suivante ou précédente. s

Remarque : ce navigateur de citations est utilisable depuis la liste de messages, le message de la fenêtre séparée de lecture, de la fenêtre de rédaction et du dialogue de vérification orthographique.

### Annonce, épellation et copie des champs de la liste de messages

Chaque ligne de la liste se décompose en plusieurs champs correspondant aux colonnes. On peut comparer un champ à une cellule d'un tableau Excel.

Les raccourcis ci-dessous s'effectuent sans changement de focus :

* chiffre 1 à 9 de la rangée au-dessus des lettres : avec le chiffre correspondant au rang de la colonne de la liste de messages, les actions suivantes sont disponibles :<br>
Un appui : annonce la valeur du champ. Par exemple, selon l'ordre de vos colonnes, 1 annonce l'expéditeur et 2 annonce le sujet.<br>
Deux appuis : épelle la valeur du champ.<br>
Trois appuis : copie la valeur du champ dans le presse-papiers.

Conseil : Si vous utilisez plusieurs dossiers, appliquez le même ordre des colonnes à tous ceux-ci, Ainsi, un chiffre correspondra toujours à la même colonne.

### Annonce et copie des entêtes du volet d'aperçu ou de la fenêtre séparée de lecture
* Alt+1 à Alt+6 depuis la liste et la fenêtre séparée de lecture :<br>
Un appui annonce la valeur de l'entête,<br>
Deux appuis ouvre une boîte d'édition contenant la valeur de l'entête. En refermant ce dialogue par Entrée, cette valeur est copiée dans le presse-papiers, ce qui est très pratique pour récupérer l'adresse mail d'un correspondant. <br>
Trois appuis ouvre le menu contextuel de l'entête concerné. C'est un menu natif de Thunderbird.

### Volet des pièces jointes dans la fenêtre principale et la fenêtre séparée de lecture
Les raccourcis suivants permettent d'annoncer les pièces jointes, de les ouvrir ou de les enregistrer.

* Alt+9 ou Alt+page down :<br>
Un appui : annonce le nombre de pièces jointes et le libellé du bouton pouvant être activé pour les ouvrir;<br>
Deux appuis : affiche le menu des actions disponible si une seule pièce jointe ou active le bouton "Tout enregistrer" si plusieurs pièces jointes sont présentes.

Remarques : 

* le volet des pièces jointes de Thunderbird 115 est en régression par rapport à celui de la version 102. Il n'y a plus de liste de pièces jointes et lorsqu'il il y a plusieurs pièces jointes, seul un bouton "Tout enregistrer" est affiché.
* Lorsqu'un bouton relatif aux pièces jointes est sélectionné, la touche Echappe simule la touche Maj+f6 pour revenir au volet précédent.

### Gestion des étiquettes depuis la liste de messages
Les raccourcis ci-dessous permettent une gestion vocalisée des étiquettes sans passer par une  navigation dans le menu contextuel de Thunderbird.

* Maj+1 à Maj+9 : Ajoute ou retire une étiquette, avec vocalisation.
* Maj+0 : Retire toutes les étiquettes du message sélectionné.
* alt+0 : Annonce toutes les étiquettes du message.

### Vocalisation des raccourcis a, c, j et m de la liste de messages
Les annonces sont différents selon qu'un seul ou plusieurs messages sont concernés par une de ces  commandes.

* a : archive les messages sélectionnés.
* c : marque les messages sélectionnés comme lu par date, avec vocalisation.<br>
* j et Maj+j : marque les messages sélectionnés comme indésirables ou acceptables.
* m : marque les messages comme lus ou non lus. 

### Raccourci alternatif pour la barre de filtrage rapide

* f : alternative ergonomique à Control+Maj+K pour afficher ou atteindre la barre de filtrage rapide. Ce raccourci est configurable dans le dialogue des gestes d'entrée (ou de commande).

### Annonce de la barre d'état et des informations de filtrage rapide
* Alt+fin ou Alt+(deuxième touche à gauche de retour arrière): 
Depuis la liste de messages ou la barre de filtrage rapide : annonce le nombre total ou filtrés de messages, le nombre de messages sélectionnés s'il y en a plus d'un  et l'expression de filtrage si un filtre a été défini. Ces informations proviennent de la barre de filtrage rapide et non plus de la barre d'état.<br>
Depuis un autre onglet ou une autre fenêtre : annonce la barre d'état.
* Lorsque la liste de messages reçoit le focus, un son ressemblant à un souffle est émis lorsqu'un filtrage rapide est actif.


### SmartReply : répondre aux listes de diffusion avec control+R 
Pour répondre à certaines listes de diffusion, il est nécessaire de presser Control+Maj+L. Pour éviter de répondre au mauvais destinataire, pressez Control+R pour répondre à la liste et deux fois Control+r pour répondre en privé à l'expéditeur du message. 

Remarque : groups.io n'est pas concerné par cette fonctionnalité.


## arborescence des dossiers

* NVDA+flèche haut : annonce le nom du dossier sélectionné. NVDA ne le fait plus par lui-même.  
* Espace sur un dossier non lu : place le focus sur le premier message non lu dans la liste de messages.
* touche entrée ou Alt+flèche haut sur un dossier : Affiche un menu permettant d'atteindre un autre dossier du même niveau d'arborescence. Ceci permet d'utiliser la première lettre des noms des dossiers. ;
* control+entrée ou Alt+flèche bas sur un dossier : Affiche un menu permettant d'atteindre un  dossier non lu du même niveau 

Ces menus comportent en outre un élément permettant de remonter au dossier parent.

Remarque :

La nouvelle structure interne de l'arborescence des dossiers ne permet plus aux extensions NVDA de la parcourir complètement à une vitesse acceptable. C'est pourquoi ces menus ne se chargent que d'un seul niveau à la fois. 

De plus, les 2 dialogues suivants qui existaient dan TBPlus 4 ont du être supprimés :

* Dialogue des Listes filtrées des compte et dossiers (F12) 
* Liste des dossiers de l'arborescence principale, selon 4 types (F7, NVDA+F7 ou Maj+F12)

## Fermeture de fenêtres et onglets
* La touche Echappe permet de fermer la fenêtre séparée de lecture d'un message et la fenêtre de rédaction. Voyez les options concernées.
* Control+Retour arrière : sert aussi à fermer les onglets et fenêtres. Lors de l'édition de texte, ce raccourci supprime le mot précédent.

## Fenêtre de rédaction
Les raccourcis de cette fenêtre concernent les champs d'adressage et le volet des pièces jointes.

* Alt+1 à Alt+8 :<br>
Un appui : annonce la valeur du champ d'adressage ou du volet des pièces jointes,<br>
Deux appuis : place le focus sur le champ d'adressage ou le volet des pièces jointes.
* Alt+pageDown : identique à Alt+3 pour le volet des pièces jointes. 
* Remarques :<br>
l'annonce du volet des pièces jointes avec Alt+3 cite une liste numérotée des noms de fichiers et leur taille totale ,<br>
Lorsque le focus se trouve dans la liste des pièces jointes, la touche échappe revient au corps du message.
* Alt+flèche haut : place le message en cours de rédaction dans le navigateur virtuel de citations ;
* Windows+flèches verticales : annonce la ligne suivante ou précédente u navigateur de citations; Ceci permet d'écouter le message auquel vous répondez sans changer de fenêtre.
* Windows+flèche horizontale : va à la citation suivante ou précédente sans changer de fenêtre.<br>

## Dialogue de vérification orthographique
A l'ouverture de ce dialogue, l'extension annonce automatiquement les mots et leur épellation. Ceci peut-être désactivé dans les options de la fenêtre de rédaction.

Les raccourcis suivants sont disponibles depuis la zone d'édition du mot de remplacement :

* Alt+flèche haut : épelle le mot mal orthographié et la proposition de remplacement. 
* Alt+flèche haut en double appui : annonce la phrase dans laquelle se trouve le mot mal orthographié, grâce au navigateur virtuel de citation qui s'initialise automatiquement dans ce contexte.
* Entrée : presse le bouton "Remplacer, sans quitter la zone d'édition.
* Maj+entrée : presse le bouton "Tout remplacer".
* Control+Entrée : presse le bouton "Ignorer".
* Maj+control+Entrée : presse le bouton "Tout ignorer".
* Alt+Entrée : ajoute le mot de remplacement au dictionnaire.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2023.10.13/thunderbirdPlusG5-2023.10.13.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=fr
