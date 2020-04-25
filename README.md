Cadre

Pour un démarrage sans éléments de bureau, avec lightdm et Raspberry Pi Desktop:
* Éditer `/etc/xdg/lxsession/LXDE-pi/autostart`
* Pour enlever la barre des tâches, commenter avec `#` la ligne `@lxpanel`
* Pour désactiver l'écran de veille, commenter la ligne `@lxscreensaver`
* Pour cacher le curseur, ajouter la ligne `@unclutter -display :0 -idle 3 -root -noevents`