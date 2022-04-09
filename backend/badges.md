# Badges

## Dimensions

Le cercle découpé doit être légèrement plus grand que la taille du badge final.

| Taille du badge | Diamètre de la découpe | Diamètre de l'image |
| :-------------- | :--------------------- | :------------------ |
| 37 mm           | 50 mm                  | 35 mm               |

## Logo

Dans paint.net

- Utiliser le fichier `badge-base.png` comme base. Il contient le cercle de découpe et un rond noir
- Insérer le logo en tant que nouveau calque
- Centrer le logo dans le rond noir, puis le mettre légèrement en haut pour laisser de la place pour le nom de l'équipe en bas
- Sauvegarder en png (flat)

Dans xnview

- Ouvrir l'image qui vient d'être sauvegardée
- Convertir l'image en binary : Image > Convert to binary > Binary (No Dither)
- Inverser les couleurs : Images > Map > Negative
- A la fin, le logo doit être blanc, le cercle noir et le fond blanc
- Sauvegarder 

Dans paint.net

- Rouvrir l'image qui vient d'être sauvegardée
- Avec la magic wand, sélectionner les 4 coins blancs autour du cercle (mettre la tolérance sur 0)
- Mettre la couleur primaire sur transparent au max (Opacity - Alpha)
- Appuyer sur backspace
- Sauvegarder en png 8 bits avec dithering au max

Dans le code

+ Déplacer le logo dans `data/badge-<année>.png`

- Mettre à jour la constante `BASE_IMAGE` avec le path vers le modèle

