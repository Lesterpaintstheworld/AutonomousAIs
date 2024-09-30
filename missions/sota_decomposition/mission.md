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



| N°                      | Utilisation                                               | Entrants                                                                                                           | Sortants                                                     | BUT                                                        | Enfants / Composants                                                        | Plan                                                                                                         | Relations clés                                                                                                                |
|------------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Utilisation (0, 1, 1) | Rédaction de l'état de l'art sur la décomposition des problèmes par les agents LLM autonomes | - Agents LLM <br> - KinOS <br> - Discord <br> - Connaissances pertinentes                                          | - Document d'état de l'art concernant la décomposition des problèmes                        | Démontrer le fonctionnement du système d'agents autonomes (KinOS)       | - Document produit <br> - Tâches décomposées <br> - Coordination entre agents                               | 1. Décomposer la tâche de rédaction en sous-tâches par KinOS <br> 2. Assigner les sous-tâches aux agents LLM <br> 3. Assurer la coordination continue entre agents <br> 4. Réviser et intégrer les différentes parties <br> 5. Vérifier la qualité et la pertinence du document produit | - KinOS assignant les tâches aux agents LLM <br> - Communication entre agents LLM via Discord <br> - Suivi de l'avancement par KinOS <br> - Accès des agents LLM aux connaissances nécessaires |
````