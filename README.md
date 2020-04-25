Cadre

Pour un démarrage sans éléments de bureau, avec lightdm et Raspberry Pi Desktop:
* Éditer `/etc/xdg/lxsession/LXDE-pi/autostart`
* Pour enlever la barre des tâches, commenter avec `#` la ligne `@lxpanel`
* Pour cacher le curseur, ajouter la ligne `@unclutter -display :0 -idle 3 -root -noevents`
* Pour désactiver l'économiseur d'écran, il est recommandé de placer le fichier `.xscreensaver` dans `$HOME`