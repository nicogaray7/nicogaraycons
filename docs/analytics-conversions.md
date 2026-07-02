# Analytics conversions - nicogaray.com + formation.nicogaray.com

## Propriete GA4 : G-L2DZPV8S00 (via GTM-54MMFRP)

## Evenements implementes

| Evenement | Declencheur | Parametres cles | Fichier |
|---|---|---|---|
| `clic_cta` | Tout clic sur un bouton ou lien CTA | `cta_label`, `cta_url`, `cta_location` | `assets/track.js` |
| `generate_lead` | Clic sur un lien `/go/rdv/` ou `calendly.com` | `lead_source`, `cta_location`, `cta_label` | `assets/track.js` |
| `scroll_paliers` | Scroll aux seuils 25/50/75/90 % | `percent_scrolled` | `assets/track.js` |
| `page_view` | Navigation (chargement de page) | `page_path`, `page_location` | Inline HTML (gtag config) |

## Quel event = quelle vente / lead

- `generate_lead` avec `lead_source = home` => lead depuis nicogaray.com (home consulting IA)
- `generate_lead` avec `lead_source = paris` (ou lyon, marseille...) => lead depuis la page ville
- `generate_lead` avec `lead_source = formation` => lead depuis formation.nicogaray.com

Le `lead_source` est extrait du parametre `?lead=` deja present dans les URLs CTA (ex. `/go/rdv/?lead=lyon`).

## Conversions a marquer manuellement dans GA4

1. Ouvrir GA4 (G-L2DZPV8S00) > Admin > Evenements
2. Chercher `generate_lead` dans la liste des evenements recus
3. Activer le toggle "Marquer comme conversion"
4. Optionnel : creer une conversion distincte par lead_source via des segments d'audience

## Verifications de proprete

- Double comptage GTM + gtag : GTM-54MMFRP est charge ET gtag config G-L2DZPV8S00 est injecte en dur dans chaque HTML. Le tag GA4 doit etre desactive dans GTM (laisser uniquement gtag direct) OU l'inverse, sinon chaque page_view compte double. **Action requise : verifier dans GTM que le tag GA4 Page View n'est pas actif.**
- Filtre IP VPS : ajouter le filtre IP 217.196.49.11 dans GA4 > Admin > Filtres de donnees (type : Adresse IP, valeur : 217.196.49.11, mode : Exclure).
- Consent Mode v2 : implementer dans les pages HTML. Le script de consentement appelle `gtag('consent', 'update', ...)` dans chaque page - c'est OK. Verifier que le consent 'default' est bien declare AVANT le chargement de GTM (actuellement c'est le cas dans index.html).

## Actions manuelles requises pour Nico dans GA4 (G-L2DZPV8S00)

- [ ] Marquer `generate_lead` comme conversion cle
- [ ] Verifier dans GTM-54MMFRP qu'il n'existe pas de tag GA4 dupliquant le page_view (desactiver si present)
- [ ] Ajouter filtre IP 217.196.49.11 (trafic interne VPS)
- [ ] Lier Google Search Console a GA4 : Admin > Liens Search Console

## Notes

- Les pages villes (lyon, paris, etc.) et formation chargent toutes `/assets/track.js`. L'ajout de `generate_lead` dans ce fichier couvre automatiquement l'ensemble du site.
- Le script inline de `formation/index.html` (lignes 659-666) tentait de capturer les clics Calendly directs mais les CTAs formation pointent vers `/go/rdv/` : ce script ne se declenchait pas. Il peut etre supprime lors d'une prochaine PR de nettoyage.
