# Thunderbird+G5 pour Thunderbird >= 115

* Auteurs: Pierre-Louis Renaud (de Thunderbird 78 à 115) & Cyrille Bougot (TB 102), Daniel Poiraud (de TB 78 à 91), Yannick (TB 45 à 60);
* URL: [Page d'accueil des extensions thunderbird+ G5 et G4][4] ;
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
* Alt+c : affiiche le menu des comptes puis le menu des dossiers du compte choisi. (2023.11.15)
* Control+Alt+c : affiiche le menu des comptes puis le menu des dossiers non lus du compte choisi. (2023.11.15)* Tab : va au volet suivant, sans détour.<br>
Note : ces deux derniers raccourcis peuvent être modifiés ou permutés via le dialogue des Gestes de commande.
* alt+Début : 1 appui sélectionne le dossier courant dans l'arborescence des dossiers, 2 appuis affiche un menu permettant de choisir le compte de messagerie à atteindre dans l'arborescence 
* Control+Alt+Début : idem mais pour les dossiers avec des messages non lus. (2023.10.31)
* Echappe : revient au volet précédent, sans détour. 
Echappe permet aussi d'alterner entre l'arborescence des dossiers et la liste de messages. 
* Maj+Tab : son comportement natif a été conservé dans cette version.

### Navigation parmi les onglets de la fenêtre principale

* Control+Tab avec ou sans la touche majuscule et control+1 à 9 : L'extension intercepte les changements d'onglet afin d'annoncer leur numéro d'ordre et le nombre total d'onglets.
* Control+la première touche située à gauche de retour-arrière : affiche un menu avec la liste des onglets existants. Pressez Entrée sur un élément de menu pour activer l'onglet correspondant.
* Alt+la première touche située à gauche de retour-arrière : affiche le menu contextuel des onglets.Ce menu est natif de Thunderbird.

Note : Le libellé de la première touche à gauche de retour-arrière varie en fonction de la langue du clavier.

## Liste de messages

<!-- begin 2023.11.10 -->

### Vocalisation personnalisée des lignes (2023.11.10)

Ce modepersonnalisé, désactivé par défaut, permet une écoute plus confortable des lignes de la liste de messages.

Il présente cependant certains inconvénients :

* Il n'est pas compatible avec la vue en fiches de la liste de messages. Pour revenir à la vue en tableau, placez vous dans la liste de messages, pressez Maj+Tab jusqu'au bouton "Options de la liste de messages", pressez Entrée et dans le menu contextuel, cochez "Vue en tableau".
* Sur les PC moins rapides, il peut provoquer un  ralentissement perceptible de la navigation avec les flèches dans la liste de messages. 
*  Le numéro de ligne sur le nombre total de lignes n'est pas annoncé.
* Si vous pressez flèche bas sur la dernière ligne, celle-ci ne sera pas annoncée.

Vous pouvez activer ce mode en pressant majuscule+puissance2 et en sélectionnant dans le menu  l'élément "Oprtions pour la fenêtre principale" puis en cochant l'option "Liste de messages :  vocalisation personnalisée des lignes".

Ce sous-menu contient également d'autres options  de personnalisation qui ne fonctionnent que si la vocalisation personnalisée est activée.
<br>
Remarque :

Certains utilisateurs rencontrent un problème de lignes vides  dans le mode normal. Si vous êtes dans ce cas, activez l'option "Liste messages : forcer le remplissage des lignes si toujours vides".

Mais idéalement, ce problème devrait être résolu en créant un nouveau profil utilisateur dans Thunderbird, ce qui implique une reconfiguration des comptes de messagerie.

#### Astuce pour la vocalisation personnalisée des lignes

Vous pouvez utiliser conjointement les deux colonnes "Statut de lecture" et "Statut" pour combiner  leurs avantages respectifs :

* La colonne "Statut de lecture" annonce "non lu" lorsque vous pressez la lettre m pour inverser le statut de lecture.
* La colonne "Statut" annonce quant à elle les statuts "Nouveau", "Répondu" et  "Transféré".
* L'extension fera en sorte que "Non lu" ne soit annoncé q'qu'une seule fois et que "Lu" ne le soit jamais.

<br>
lisez aussi la section [Choix et agencement des colonnes](#cols) 

### Raccourcis de la liste de messages

<!-- end 2023.11.10 -->

* Echappe dans la liste de messages : si un filtre est actif, il est désactivé et la liste de messages reste sélectionnée. Sinon, ce raccourci donne le focus à l'arborescence des dossiers.
* NVDA+flèche haut dans la liste de messages :<br>
Un appui : annonce la ligne courante de la liste de messages. Le raccourci NVDA+Tab produit le même résultat mais sans passer par cette extension.<br>
Deux appuis : affiche le détail de la ligne dans une fenêtre de texte qui permet l'analyse de la ligne au clavier.
* Espace, F4 ou Alt+flèche bas : lit une version épurée du message du volet d'aperçu, sans quitter la liste de messages.
* Alt+flèche haut : place le message dans le navigateur virtuel de citations ;
* Windows+flèches bas ou haut : lit la citation suivante ou précédente.

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

* Alt+9 ou Alt+page suivante :<br>
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

### Vocalisation des raccourcis  a, c, j et m de la liste de messages

A partir de la version 2023.11.10, ces raccourcis de marquage ne sont plus vocalisés par l'extension. NVDA annonce immédiatement le changement de contenu de la ligne concernée.

### Filtrage rapide de messages (2023.11.10)

lettre f : alternative ergonomique à Control+Maj+k pour afficher ou atteindre la barre de filtrage rapide. Ce raccourci est configurable dans le dialogue des gestes de commande.
<br>Note : Le focus doit se trouver dans une liste de messages non vide. Pressez Echappe pour désactiver le filtre actif.

Pour accéder directement aux résultats du filtrage depuis le champ de saisie du mot-clé, pressez flèche bas.

Lorsqu'un filtre est actif,  un son ressemblant à un souffle  est joué chaque fois  que la liste de messages obtient le focus. Ceci est surtout utile  lorsque vous changez de fenêtre ou d'onglet puis que vous revenez plus tard à la liste de messages.

Si ce son vous dérange, vous avez deux possibilités :

1. Ouvrez le menu Majuscule+(touche au-dessus de Tab) et dans le sous-menu de Désactivation, cochez l'option :<br>
Liste messages : ne pas jouer un son lorsque la liste est filtrée et obtient le focus.

2. Ouvrez le menu Majuscules+(touche au-dessus de Tab) puis pressez Entrée sur l'élément : Ouvrir le dossier des sons. 
<br>Ce dossier s'ouvrira dans l'Explorateur de fichiers,
<br>Vous y trouverez le fichier filter.wav.
<br> Vous pouvez remplacer ce fichier par un autre pour autant que votre fichier porte le même nom : filter.wav.
<br>Cela fait, redémarrez NVDA.

<!-- end 2023.10.31 -->

### Annonce de la barre d'état et des informations de filtrage rapide
* Alt+fin ou Alt+(deuxième touche à gauche de retour arrière): 
Depuis la liste de messages ou la barre de filtrage rapide : annonce le nombre total ou filtrés de messages, le nombre de messages sélectionnés s'il y en a plus d'un  et l'expression de filtrage si un filtre a été défini. Ces informations proviennent de la barre de filtrage rapide et non plus de la barre d'état.<br>
Depuis un autre onglet ou une autre fenêtre : annonce la barre d'état.
* Lorsque la liste de messages reçoit le focus, un son ressemblant à un souffle est émis lorsqu'un filtrage rapide est actif.


### SmartReply : répondre aux listes de diffusion avec control+R 
Pour répondre à certaines listes de diffusion, il est nécessaire de presser Control+Maj+L. Pour éviter de répondre au mauvais destinataire, pressez Control+R pour répondre à la liste et deux fois Control+r pour répondre en privé à l'expéditeur du message. 

Remarque : groups.io n'est pas concerné par cette fonctionnalité.

<a name="cols">
<!-- begin 2023.10.31 -->

###  Choix et agencement des colonnes (2023.10.31)

Cette procédure est native de Thunderbird 115 mais elle est expliquée ici car elle est mal documentée.

* Pressez Maj+tab depuis la liste de messages  pour gous placer dans la liste des entêtes de colonnes.
* Utilisez  les flèches gauche et droite  pour sélectionner une colonne.
* Lorsque vous atteingnez la colonne spéciale "Choisir les colonnes à afficher", pressez entrée dessus.
* Dans le menu, cochez ou décochez des colonnes puis pressez Echappe pour fermer ce menu. 
* De retour dans  la liste des entêtes de colonnes, pressez flèche gauche  jusqu'à une   colonne à déplacer.
* Pressez ensuite Alt+flèche gauche ou droite pour la placer à l'endroit désiré. Ceci sera correctement vocalisé.
* Répétez ces opérations pour déplacer d'autres colonnes.
* Quand l'organisation des colonnes est terminée, presser Tab pour revenir  à la liste de messages.

## arborescence des dossiers : navigation rapide (2023.10.31)

Certaines commandes affichent un menu reprenant des dossiers de l'arborescence pour permettre une navigation par lettres initiales. Pour des raisons de performances,  le script n'affiche pas les sous-dossiers des branches réduites.

De plus, si le nom d'un compte ou dossier  se termine par un tiret, celui-ci ne sera pas inclu dans le menu des dossiers non lus. 

Il est donc conseillé  d'exclure des comptes et dossiers en refermant des branches peu utilisées ou en renommant des comptes pour ajouter un tiret à la fin de leur nom.

Commandes disponibles  dans l'arborescence des dossiers :

* NVDA+flèche haut : annonce le nom du dossier sélectionné. NVDA ne le fait plus par lui-même.  
* Espace sur un dossier non lu : place le focus sur le premier message non lu dans la liste de messages.
* Entrée  ouAlt+flèche haut : affiche un menu de tous les dossiers du compte auquel le dossier sélectionné appartient.
* Control+Entrée ou Alt+flèche bas : affiche un menu des dossiers non lus du compte auquel le dossier sélectionné appartient.
<br>Dans les deux cas, le dernier élément du menu permet d'afficher le menu des comptes. Vous pouvez presser la barre d'espace pour choisir un compte à partir de là.
* Maj+Entrée :  affiche un menu contenant tous les comptes et dossiers de l'arborescence.
* Maj+Control+Entrée :  affiche un menu contenant tous les comptes et dossiers non lus de l'arborescence.

Remarques :

Pour ces deux dernières commandes, un certain temps sécoulera avant l'affichage du menu car lle script doit parcourir toute l'arborescence pour construire le menu.

Utilisez plutôt une de ces deux  petites astuces :

1. Pressez  Alt+Début  deux fois rapidement pour afficher le menu des comptes, 
<br>Choisissez un  compte puis pressez Entrée. 
<br>Un nouveau menu contenant les dossiers de ce compte  s'ouvrira et vous pourrez utiliser une lettre pour en activer un.
2. Pressez  Control+Alt+Début  deux fois rapidement pour afficher le menu des comptes avec des dossiers non lus, 
<br>Choisissez un  compte puis pressez Entrée. 
<br>Un nouveau menu contenant les dossiers non lus de ce compte  s'ouvrira et vous pourrez utiliser une lettre pour en activer un.

<!-- end 2023.10.31 -->

## Fermeture de fenêtres et onglets
* La touche Echappe permet de fermer la fenêtre séparée de lecture d'un message et la fenêtre de rédaction. Voyez les options concernées.
* Control+Retour arrière : sert aussi à fermer les onglets et fenêtres. Lors de l'édition de texte, ce raccourci supprime le mot précédent.

## Fenêtre de rédaction
Les raccourcis de cette fenêtre concernent les champs d'adressage et le volet des pièces jointes.

* Alt+1 à Alt+8 :<br>
Un appui : annonce la valeur du champ d'adressage ou du volet des pièces jointes,<br>
Deux appuis : place le focus sur le champ d'adressage ou le volet des pièces jointes.
* Alt+page suivante : identique à Alt+3 pour le volet des pièces jointes. 
* Remarques :<br>
l'annonce du volet des pièces jointes avec Alt+3 cite une liste numérotée des noms de fichiers et leur taille totale ,<br>
Lorsque le focus se trouve dans la liste des pièces jointes, la touche échappe revient au corps du message.
* Alt+flèche haut : place le message en cours de rédaction dans le navigateur virtuel de citations ;
* Windows+flèches verticales : annonce la ligne suivante ou précédente du navigateur de citations; Ceci permet d'écouter le message auquel vous répondez sans changer de fenêtre.
* Windows+flèche horizontale : va à la citation suivante ou précédente sans changer de fenêtre.<br>

## Dialogue de vérification orthographique
A l'ouverture de ce dialogue, l'extension annonce automatiquement les mots et leur épellation. Ceci peut-être désactivé dans les options de la fenêtre de rédaction.

Les raccourcis suivants sont disponibles depuis la zone d'édition du mot de remplacement :

* Alt+flèche haut : épelle le mot mal orthographié et la proposition de remplacement. 
* Alt+flèche haut en double appui : annonce la phrase dans laquelle se trouve le mot mal orthographié, grâce au navigateur virtuel de citation qui s'initialise automatiquement dans ce contexte.
* Entrée : presse le bouton "Remplacer", sans quitter la zone d'édition.
* Maj+entrée : presse le bouton "Tout remplacer".
* Control+Entrée : presse le bouton "Ignorer".
* Maj+control+Entrée : presse le bouton "Tout ignorer".
* Alt+Entrée : ajoute le mot déclaré comme mal orthographié au dictionnaire.


## Compléments externes

### Extension Start With inbox pour Thunderbird 115 (2023.10.31)1

Au démarrage de Thunderbird, Cette extension   sélectionne   automatiquement au choix :

* le  dossier "Courrier entrant" du compte de votre choix dans larborescence des dossiers.
* Le dernier message du dossier courrier entrant du compte choisi. 
* Le premier  message non lu du dossier courrier entrant du compte choisi. 

Installation :

* dans Thunderbird, ouvrez le menu "Outils" puis validez sur : Modules complémentaires et thèmes ;
* Dans la page du Gestionnaire de modules,, placez-vous dans le champ de recherche. En mode navigation, vous pouvez presser la lettre e pour l'atteindre rapidement ;
* écrivez : Start with Inbox puis pressez Entrée ;
* sélectionnez manuellement l'onglet "Start with inbox :: Recherche :: Modules pour Thunderbird" par exemple.   pressez ensuite la touche 3 ou guillemet jusqu'à atteindre le titre de niveau 3 intitulé par le nom du module que vous avez recherché ; 
* Avec la flèche bas, Descendez  jusqu'au lien "Ajouter à Thunderbird" puis pressez Entrée dessus ;
* Suivez la procédure puis redémarrez Thunderbird ;
* Si tout s'est bien passé, Thunderbird s'ouvrira sur l'onglet principal et donnera le focus à la liste de messages ;


Régler les options de Start with Inbox :

* Retournez dans l'onglet "Gestionnaire de modules complémentaires" ;
* Le cas échéant, quittez le champ de recherche afin de vous placer en mode navigation ;
* Pressez autant de fois que nécessaire la touche 3 pour atteindre le titre de niveau 3 intitulé    "Start with Inbox dans la liste des modules installés ;
* Validez ensuite sur le bouton : Options des modules. Ceci ouvre un nouvel onglet intitulé : Start with Inbox, Settings ;
*  Réglez les options puis redémarrez Thunderbird.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2023.11.15/thunderbirdPlusG5-2023.11.15.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=fr

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=fr
