Usage: ./bin/generate_qna_chunk.sh PROMPT_PATH
Usage: ./bin/generate_qna_crawl.sh PROMPT_PATH
PROMPT_PATH: path were you can find the user and system prompt for the openai API and the JSON template.

## Example command
```
./bin/generate_qna_crawl.sh ailab/db/finesse/prompt
```

La génération de questions se déroule en trois parties. Premièrement, nous récupérons une page aléatoire « crawl », dans la base de données (aléatoire mais triée en fonction d'une valeur de score précise). Ensuite, nous utilisons un modèle pour expliquer à ChatGPT ce qu'il doit faire (dans notre cas, prendre toutes les données, les analyser, puis générer une question et une réponse). Une fois toutes ces étapes accomplies, nous stockons toutes les données dans un fichier JSON et nous traitons un prochain document. Ce code est très utile pour générer toutes sortes de tests, et je l'ai réalisé pour qu'il soit le plus réutilisable possible. Si nous souhaitons changer les instructions ou les modèles, nous pouvons simplement en appeler d'autres lors de l'exécution de la fonction (il est préférable d'utiliser le script en bash plutôt qu'en python pour appeler le code).
Nous pouvons lancer le code pour chercher en fonction des « chunks » ou des « crawls ». Je conseille fortement d’utiliser la recherche par crawl car, n’ayant pas trouvé de score pour les chunks (je ne peux garantir leur existence), la recherche par crawl génère donc de meilleures questions.
Pour ce qui est de la récupération de données, il sera peut-être nécessaire de modifier le code pour s'adapter au mieux à un nouveau cas. Quant au nombre de questions générées, il suffit de modifier la variable globale en haut du script.
