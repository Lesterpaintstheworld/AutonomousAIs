Mission
============
````
je souhaite rédiger un état de l'art sur la décomposition des problèmes par les agents LLM autonomes pour permettre leur résolution, afin de démontrer que notre système d'agents autonomes (KinOS) fonctionne. 

L'état de l'art doit utiliser uniquement son espace latent, Discord pour la coordination entre les agents, et le KinOS (codé sur n8n)

Plan proposé (conditions à respecter) :

Caractéristiques des systèmes entrants :
a. Agents LLM : capables de comprendre et synthétiser des informations complexes
b. KinOS : fonctionnel pour la coordination des agents et la décomposition des tâches
c. Discord : configuré pour permettre la communication entre les agents
d. Connaissances : à jour et pertinentes sur la décomposition des problèmes par les agents autonomes
Relations entre les systèmes :
a. KinOS doit pouvoir assigner des tâches spécifiques à chaque agent LLM
b. Les agents LLM doivent pouvoir communiquer entre eux via Discord
c. KinOS doit pouvoir suivre l'avancement global de la rédaction
d. Les agents LLM doivent pouvoir accéder aux connaissances nécessaires pour la rédaction
Conditions de réalisation :
a. Décomposition de la tâche de rédaction en sous-tâches par KinOS
b. Attribution des sous-tâches aux agents LLM appropriés
c. Coordination continue entre les agents pour assurer la cohérence du document final
d. Révision et intégration des différentes parties de l'état de l'art
e. Vérification finale de la qualité et de la pertinence du document produit



| N°         | Utilisation                                                                                                                     | Entrants                                                                                                          | Sortants                                                                                                                | BUT                                                                                                                                           | Enfants / Composants                                                      | Plan                                                                                                                                                                                                                                                                    | Relations clés                                                                                  |
|------------|-------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| (0, 1, 1)  | Rédaction d'un état de l'art sur la décomposition des problèmes par agents LLM autonomes                                        | Agents LLM, KinOS, Discord, Connaissances sur décomposition des problèmes                                          | Document d'état de l'art sur la décomposition des problèmes                                                            | a) Produire un document cohérent sur la décomposition<br>b) Démontrer la fonctionnalité de KinOS et des agents autonomes dans cette tâche | Document d'état de l'art                                                   | a) Décomposer la tâche en sous-tâches<br>b) Assigner les sous-tâches aux agents LLM<br>c) Assurer la communication via Discord<br>d) Réviser et intégrer les sous-parties<br>e) Vérifier qualité et pertinence du document final                                                       | a) KinOS assigne des tâches aux agents LLM<br>b) Communication entre agents via Discord                                                            |
````