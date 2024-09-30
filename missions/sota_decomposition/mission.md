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



| N°             | Utilisation                                                                                                         | Entrants                                                                                     | Sortants                                                                                                    | BUT                                                                                                                                              | Enfants / Composants                                                                                          | Plan                                                                                                                                                                                                                                                                                                       | Relations clés                                                                            |
|-----------------|--------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| (0, 1, 1)       | Rédaction de l'état de l'art sur la décomposition des problèmes par agents LLM autonomes                             | Agents LLM, KinOS, Discord, Connaissances sur décomposition de problèmes                   | Document d'état de l'art                                                                                   | a) Rédiger un document cohérent et structuré. <br> b) Assurer que le document démontre l'efficacité de KinOS pour la coordination des agents.      | Document rédigé                                                                                              | a. KinOS décompose la tâche d'écriture en sous-tâches.<br> b. Chaque sous-tâche est assignée à un ou plusieurs agents LLM en fonction de leurs capacités.<br> c. Les agents LLM collaborent via Discord pour maintenir la cohérence.<br> d. Les parties rédigées sont intégrées dans un document unique. <br> e. Finalisation et vérification de qualité. | a) KinOS coordonne les agents LLM pour la rédaction.<br> b) Communication entre agents via Discord.<br> c) Suivi de l'avancement par KinOS.<br> d) Accès aux connaissances pour tous les agents.  |
````