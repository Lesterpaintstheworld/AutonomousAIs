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



## Décomposition de Niveau 0 - Mission "missions/sota_decomposition"

### Utilisation (0, 1, 1)
- **Utilisation :** Rédaction de l'état de l'art sur la décomposition des problèmes par les agents LLM autonomes pour démontrer le fonctionnement de KinOS.
- **Entrants :** 
  - Agents LLM (capables de comprendre et synthétiser des informations complexes)
  - KinOS (fonctionnel pour la coordination des agents et la décomposition des tâches)
  - Discord (configuré pour permettre la communication entre les agents)
  - Connaissances (à jour et pertinentes sur la décomposition des problèmes par les agents autonomes)
- **Sortants :** État de l'art rédigé sur la décomposition des problèmes par les agents LLM autonomes.
- **BUT :** Démontrer le fonctionnement efficace des agents autonomes au sein de KinOS.
- **Enfants / Composants :** 
  - Sous-tâches de rédaction
  - Tâches attribuées aux agents LLM
  - Coordination des communications via Discord
  - Révisions des parties de l'état de l'art
- **Plan :**
  1. Décomposition de la tâche de rédaction en sous-tâches par KinOS.
  2. Attribution des sous-tâches aux agents LLM appropriés.
  3. Coordination continue entre les agents pour assurer la cohérence du document final.
  4. Révision et intégration des différentes parties de l'état de l'art.
  5. Vérification finale de la qualité et de la pertinence du document produit.
- **Relations clés :** 
  - KinOS attribue des tâches spécifiques à chaque agent LLM.
  - Les agents LLM communiquent entre eux via Discord.
  - KinOS suit l'avancement global de la rédaction.
  - Les agents LLM accèdent aux connaissances nécessaires pour la rédaction.
````