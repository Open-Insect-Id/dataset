La fonction `tree` (dans `utility_scripts/tree.py`) parcourt récursivement l'arborescence du dossier passé en argument. Utile pour vérifier le bon transfert des fichiers, en utilisant un programme permettant la comparaison de l'arborescence exportée avec celle exécutée localement avant l'upload du dataset. Ayant eu des coupures d'Internet durant l'upload, il fallait que je m'assure que les fichiers aient tous été correctement transférés.

Note : Ce programme n'a pas pour but de vérifier l'intégrité des images, ce qui se révélera être un vrai problème par la suite. En effet, avec les interruptions d'Internet, certaines images ont été corrompues durant le transfert, et il m'a fallu longtemps avant de m'en rendre compte.

---

<div style="text-align: center;">
    <img src="https://github.com/Open-Insect-Id/dataset/blob/main/taxonomie_schema.webp?raw=true" width="500" alt="Classification taxonomique">
</div>

---

Image représentant la **classification taxonomique**, qui permet d'atteindre une **précision maximale**, et également de **réduire l'erreur** : si le modèle se trompe sur l'espèce, l'ordre, la famille et le genre ont de fortes chances d'être corrects, réduisant ainsi l'impact de l'erreur, par rapport à un modèle qui ne prédirait que l'espèce finale.

**Voici un exemple de chemin de fichier d'une image, depuis laquelle nous extrayons la classification taxonomique.**

```train/train/00980_Animalia_Arthropoda_Insecta_Lepidoptera_Erebidae_Arctia_virginalis/464f3a34-4c04-4eb3-afa2-6cb7444c3fa3.jpg```

Ici nous avons un insecte (critère ayant permis de ne sélectionner que les insectes du dataset original), de l'ordre **Lepidoptera**, de la famille **Erebidae**, de genre **Arctia** et d'espèce **virginalis**. Si nous avions choisi de ne sauver que l'espèce, le modèle aurait peut-être gagné un peu en précision (moins de données à absorber) mais en cas d'erreur du modèle, rien n'aurait alors été vrai. Dans une logique de réduction de l'impact de l'erreur, nous choisirons donc de conserver **4 informations taxonomiques** : **l'ordre**, **la famille**, **le genre** et **l'espèce**.
Nous nommerons par la suite ***'taxon'*** le groupe d'informations taxonomiques.

Dans un premier temps la fonction `parse_taxonomy` (dans `utility_scripts/taxonomy.py`) extrait le nom du dossier parent de l'image, car le nom de l'image en elle-même ne contient pas d'informations.

Taxon folder: ```00980_Animalia_Arthropoda_Insecta_Lepidoptera_Erebidae_Arctia_virginalis```

Bien, il nous suffit maintenant d'extraire les informations taxonomiques de ce nom, à l'aide de la méthode split(), qui retourne une liste, dont les éléments sont ici séparés par un *underscore* (_). Les informations 0 (ID unique), 1, 2, 3 (constantes sur ce dataset filtré) ne nous intéressent pas, nous nous contentons alors de créer un dictionnaire avec les clés suivantes : `ordre`, `famille`, `genre` et `espece`.

Résultat: {'ordre': 'Lepidoptera', 'famille': 'Erebidae', 'genre': 'Arctia', 'espece': 'virginalis'}

La fonction `verify_image_validity` (dans `utility_scripts/corruption_scan.py`) a été rajoutée ici après un premier entrainement complet, car nous expérimentions alors des erreurs dont l'origine était difficile à trouver : la corruption d'images, qui ayant servies à entrainer le modèle, introduisait des erreurs dans les prédictions, par exemple en donnant un ordre et une famille, puis un genre et une espèce n'existant pas sous la famille donnée. Il s'avère que nous ne pouvons malheureusement pas éliminer ces images du dataset, puisque c'est l'une des limitations de Kaggle, le dossier qui sert d'input est en lecture seule. Pour contourner le problème, nous allons alors écrire dans un fichier la liste des fichiers corrompus par avance, puis lors de l'entrainement final, nous ajouterons une vérification pour ne pas traiter les images dont le chemin apparait dans cette liste. 