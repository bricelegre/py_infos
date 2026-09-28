# presentation/modules.py
"""Contenu des pages de présentation des modules de Fincompta.

Chaque module est décrit une seule fois ici et affiché par le gabarit
commun presentation/details-module.html. Le contenu suit ce que fait
réellement l'application fincompta, formule par formule :

- "all"     : inclus dans toutes les formules (Free, Starter, Premium) ;
- "paid"    : formules payantes uniquement (Starter et Premium) ;
- "premium" : formule Premium uniquement ;
- "asso"    : offre Association/ONG uniquement.

L'offre Association/ONG repose sur une application distincte, syscebnl
(plan comptable et états SYCEBNL). ASSO_AVAILABILITY indique, module par
module, ce qu'elle reprend de fincompta ; syscebnl n'applique pas de
restriction par formule.

Ces niveaux reprennent FEATURE_MIN_PLAN_LEVEL (fincompta/payment/services.py) :
à tenir à jour ensemble.
"""

PLAN_LABELS = {
    "all": "Toutes formules",
    "paid": "Starter & Premium",
    "premium": "Premium",
    "asso": "Association/ONG",
}

PLAN_AVAILABILITY = {
    "all": "Free, Starter, Premium",
    "paid": "Starter, Premium",
    "premium": "Premium",
    "asso": "Association/ONG",
}

# Disponibilité de chaque module dans l'offre Association/ONG (syscebnl) :
# None = module absent ; sinon texte affiché sur la page du module.
ASSO_AVAILABILITY = {
    "comptabilite": "Inclus, avec le plan comptable SYCEBNL. Sans import des ventes E-impôt ni "
                    "comptabilisation groupée de la paie.",
    "tresorerie": "Journal de caisse inclus. Sans état de caisse ni rapport mensuel par e-mail.",
    "facturation": None,
    "crm": None,
    "grh": "Inclus.",
    "paie": "Inclus. Comptabilisation bulletin par bulletin.",
    "etats": "Inclus, avec en plus les états SYCEBNL : bilan, tableau emplois-ressources, "
             "exécution budgétaire et notes annexes.",
    "budget": None,
    "audit": "Inclus, avec 23 contrôles dont 9 propres au SYCEBNL.",
    "prospection": None,
}


MODULES = {
    # ------------------------------------------------------------------ Comptabilité
    "comptabilite": {
        "url_name": "presentation:details-comptabilite",
        "name": "Comptabilité",
        "icon": "bi-journal-text",
        "plan": "all",
        "summary": (
            "Saisie des opérations, imports, comptabilisation automatique de la caisse, "
            "de la facturation et de la paie, lettrage et recherche."
        ),
        "lead": (
            "Une comptabilité SYSCOHADA révisé tenue à jour sans ressaisie : les opérations de caisse, "
            "les factures et les bulletins de paie sont comptabilisés automatiquement, les écritures "
            "sont contrôlées à la saisie et les comptes de tiers se lettrent par compte collectif."
        ),
        "badges": ["Conforme SYSCOHADA révisé", "Plan comptable pré-installé"],
        "headline": "Des écritures fiables, saisies une seule fois",
        "subtitle": (
            "Le plan comptable et les journaux sont installés dès la création du compte. Vous saisissez "
            "ou importez vos opérations, Fincompta génère le reste des écritures depuis les autres modules."
        ),
        "steps": [
            ("Paramétrage", "Plan comptable SYSCOHADA révisé pré-installé, journaux comptables, comptes de "
             "tiers rattachés à leur compte collectif (411, 401…), types de dépenses de caisse."),
            ("Saisie & imports", "Saisie des opérations par pièce (journal, comptes, tiers, débit/crédit), ou "
             "import Excel des écritures et des factures de vente E-impôt."),
            ("Comptabilisation automatique", "Opérations de caisse, factures, bulletins de paie et écritures "
             "récurrentes passent en comptabilité sans ressaisie."),
            ("Contrôle & lettrage", "Équilibre débit/crédit, recherche d'opérations par pièce ou référence, "
             "lettrage des comptes de tiers."),
            ("États & clôture", "Balance, grand livre tiers, compte d'exploitation, puis clôture de "
             "l'exercice avec génération des reports à nouveau."),
        ],
        "tabs": [
            ("Saisie & imports", [
                ("bi-journal-text", "Saisie des opérations",
                 "Saisie par pièce avec journal, compte débit/crédit, compte de tiers et libellé ; modification "
                 "et suppression sécurisées.", "all"),
                ("bi-file-earmark-arrow-up", "Import des écritures (Excel)",
                 "Modèle Excel fourni, mode test sans enregistrement, option de remplacement des écritures "
                 "déjà importées.", "paid"),
                ("bi-receipt-cutoff", "Import des ventes E-impôt",
                 "Import du fichier des factures de vente : HT, TVA, autres taxes et TTC comptabilisés par "
                 "client.", "paid"),
                ("bi-arrow-repeat", "Écritures récurrentes",
                 "Modèles d'écritures pour les charges qui reviennent chaque mois (loyer, internet, "
                 "assurance…).", "paid"),
            ]),
            ("Comptabilisation automatique", [
                ("bi-cash-stack", "Caisse",
                 "Chaque entrée ou sortie de caisse génère son écriture selon le type d'opération choisi.", "all"),
                ("bi-receipt", "Factures",
                 "Comptabilisation d'une facture en un clic depuis la facturation : client, HT, TVA, TTC.", "all"),
                ("bi-person-vcard", "Bulletins de paie",
                 "Écriture de paie (salaires, charges sociales et fiscales, avances et prêts) générée depuis "
                 "le bulletin.", "all"),
                ("bi-collection", "Paie du mois en un clic",
                 "Bouton « Tout comptabiliser » : toutes les paies non comptabilisées du mois en une fois.",
                 "paid"),
            ]),
            ("Contrôle & tiers", [
                ("bi-shield-check", "Contrôles à la saisie",
                 "Équilibre débit = crédit, comptes et tiers vérifiés, avertissement si le tiers ne correspond "
                 "pas au compte.", "all"),
                ("bi-link-45deg", "Lettrage",
                 "Lettrage des comptes de tiers par compte collectif (411, 401…) plutôt que sous-compte par "
                 "sous-compte.", "all"),
                ("bi-search", "Recherche d'opérations",
                 "Retrouvez une écriture par numéro de pièce ou référence et accédez directement à sa "
                 "modification.", "all"),
                ("bi-people", "Comptes de tiers",
                 "Tiers actifs ou suspendus, détection des doublons, compte de rattachement proposé à la "
                 "saisie et à l'import.", "all"),
            ]),
        ],
        "form_hint": "Décrivez : volume d'écritures, journaux, imports à prévoir, reprise d'historique…",
    },

    # ------------------------------------------------------------------ Trésorerie
    "tresorerie": {
        "url_name": "presentation:details_tresorerie",
        "name": "Trésorerie & Caisse",
        "icon": "bi-cash-coin",
        "plan": "all",
        "summary": (
            "Journal de caisse, pièces justificatives, comptabilisation automatique, états de caisse "
            "et rapport mensuel du dirigeant par e-mail."
        ),
        "lead": (
            "Tenez votre caisse au jour le jour : chaque entrée ou sortie est rattachée à un type "
            "d'opération et à ses pièces justificatives, puis comptabilisée automatiquement. Vous "
            "recevez l'état de caisse et un rapport mensuel clair par e-mail."
        ),
        "badges": ["Caisse & banque", "Rapport mensuel par e-mail"],
        "headline": "Votre caisse tenue au quotidien, votre trésorerie lisible",
        "subtitle": (
            "Plus besoin de cahier de caisse ni de ressaisie en comptabilité : la caisse alimente "
            "directement les journaux et les indicateurs de trésorerie."
        ),
        "steps": [
            ("Types d'opération", "Paramétrez vos types de dépenses et de recettes : chacun porte ses "
             "comptes de débit et de crédit."),
            ("Saisie de la caisse", "Enregistrez les entrées et sorties du jour avec n° de pièce, tiers "
             "et libellé."),
            ("Pièces justificatives", "Joignez les pièces (reçus, factures) à chaque opération."),
            ("Comptabilisation", "L'écriture est générée automatiquement ; un bordereau comptable "
             "imprimable accompagne chaque opération."),
            ("Suivi", "Solde de caisse, état de caisse par e-mail et rapport mensuel du dirigeant."),
        ],
        "tabs": [
            ("Caisse", [
                ("bi-cash-stack", "Journal de caisse",
                 "Entrées et sorties par jour et par mois, avec n° de pièce, tiers et type d'opération.", "all"),
                ("bi-tags", "Types d'opération",
                 "Chaque type d'opération sait quels comptes mouvementer : pas de schéma comptable à "
                 "connaître.", "all"),
                ("bi-paperclip", "Pièces justificatives",
                 "Les justificatifs restent attachés à l'opération et consultables à tout moment.", "all"),
                ("bi-printer", "Bordereau comptable",
                 "Ticket imprimable avec journal, compte débit et compte crédit de l'opération.", "all"),
            ]),
            ("Suivi & rapports", [
                ("bi-envelope-paper", "État de caisse par e-mail",
                 "Solde de départ, total des recettes, total des dépenses et mouvements des autres journaux.",
                 "all"),
                ("bi-graph-up-arrow", "Rapport mensuel du dirigeant",
                 "Chaque mois : avez-vous gagné de l'argent ? combien avez-vous ? qui vous doit ? vos salariés "
                 "et ce qu'il faut déclarer et payer.", "all"),
                ("bi-bank", "Trésorerie nette",
                 "Disponible en caisse, banques et mobile money, suivi dans les états et les analyses.", "all"),
                ("bi-arrow-left-right", "Virements internes",
                 "Les virements caisse ↔ banque sont suivis et leurs écarts signalés.", "all"),
            ]),
        ],
        "form_hint": "Décrivez : nombre de caisses, volume d'opérations, banques et mobile money utilisés…",
    },

    # ------------------------------------------------------------------ Facturation
    "facturation": {
        "url_name": "presentation:detail_facturation_crm",
        "name": "Facturation",
        "icon": "bi-receipt",
        "plan": "all",
        "summary": (
            "Devis et factures (HT, TVA, TTC), PDF avec QR code de vérification, envoi par e-mail, "
            "paiements partiels et comptabilisation en un clic."
        ),
        "lead": (
            "Émettez vos devis et factures en quelques clics, envoyez-les par e-mail, suivez les "
            "règlements et les impayés, puis comptabilisez chaque facture sans ressaisie."
        ),
        "badges": ["Devis & factures", "QR code d'authenticité"],
        "headline": "Du devis à l'encaissement, sans ressaisie",
        "subtitle": (
            "Les clients sont partagés avec la comptabilité et le CRM : une facture émise est suivie "
            "jusqu'à son règlement et à sa comptabilisation."
        ),
        "steps": [
            ("Clients", "Fiche client commune à la facturation, au CRM et à la comptabilité."),
            ("Devis", "Lignes de prestation, quantités, prix unitaires, remise, TVA et autres taxes."),
            ("Facture", "Conversion du devis en facture, n° de bon de commande, échéance et modalité de "
             "paiement."),
            ("Envoi & encaissement", "PDF envoyé par e-mail, règlements partiels et reste dû suivis."),
            ("Comptabilisation", "La facture passe en comptabilité en un clic."),
        ],
        "tabs": [
            ("Devis & factures", [
                ("bi-file-earmark-text", "Devis et factures",
                 "Désignation, quantité, prix unitaire, remise, HT, TVA, autres taxes et TTC calculés.", "all"),
                ("bi-arrow-left-right", "Conversion devis → facture",
                 "Un devis accepté devient une facture sans rien ressaisir.", "all"),
                ("bi-qr-code", "PDF avec QR code",
                 "Chaque document porte un QR code qui permet à votre client de vérifier son authenticité.",
                 "all"),
                ("bi-envelope", "Envoi par e-mail",
                 "Envoi du devis ou de la facture au client directement depuis Fincompta.", "all"),
            ]),
            ("Suivi & reporting", [
                ("bi-wallet2", "Paiements partiels",
                 "Plusieurs règlements par facture, montant déjà réglé et reste dû toujours à jour.", "all"),
                ("bi-exclamation-triangle", "Factures échues",
                 "Liste des factures échues et non payées, avec le retard et le reste dû par client.", "all"),
                ("bi-speedometer2", "Tableau de bord",
                 "CA HT, TVA et TTC du mois et de l'année, nombre de ventes, opportunités ouvertes.", "all"),
                ("bi-filetype-pdf", "Rapport Facturation & CRM",
                 "Rapport mensuel PDF : ventes comptabilisées, créations et activités commerciales du mois.",
                 "all"),
            ]),
        ],
        "form_hint": "Décrivez : nombre de factures par mois, taxes appliquées, besoin d'envoi par e-mail…",
    },

    # ------------------------------------------------------------------ CRM
    "crm": {
        "url_name": "presentation:detail_crm",
        "name": "CRM",
        "icon": "bi-people",
        "plan": "all",
        "summary": (
            "Clients et prospects, activités, opportunités, pipeline Kanban, prévisions de ventes "
            "et statistiques d'équipe."
        ),
        "lead": (
            "Suivez vos clients et prospects, planifiez les activités de vos commerciaux, faites "
            "avancer les opportunités dans le pipeline et anticipez vos ventes des six prochains mois."
        ),
        "badges": ["Pipeline Kanban", "Prévisions pondérées"],
        "headline": "Une vision claire de votre activité commerciale",
        "subtitle": (
            "Le CRM partage ses clients avec la facturation : de la première activité à la facture "
            "réglée, tout l'historique est au même endroit."
        ),
        "steps": [
            ("Clients & prospects", "Fiche entreprise (RCCM, n° de compte contribuable, contacts) et "
             "historique complet."),
            ("Activités", "Appels, rendez-vous, relances : chaque commercial suit ses activités et tâches."),
            ("Opportunités", "Montant, probabilité, échéance prévue et étape du pipeline."),
            ("Pipeline", "Vue Kanban : faites glisser une opportunité d'une étape à l'autre, gagnée ou "
             "perdue (avec la raison)."),
            ("Prévisions", "Prévision mensuelle pondérée et statistiques d'équipe."),
        ],
        "tabs": [
            ("Clients & activités", [
                ("bi-building", "Clients & prospects",
                 "Fiche entreprise, timeline des échanges, factures et synthèse par client.", "all"),
                ("bi-calendar-check", "Activités & tâches",
                 "Mes activités, toutes les activités de l'équipe, tâches assignées et échéances.", "all"),
                ("bi-cart-check", "Ventes",
                 "Ventes par client et par commercial, reste dû échu et retard maximum.", "all"),
                ("bi-filetype-pdf", "Rapport d'activité",
                 "Rapport PDF des activités commerciales du mois.", "all"),
            ]),
            ("Opportunités & prévisions", [
                ("bi-kanban", "Pipeline Kanban",
                 "Étapes du pipeline, probabilité, montant pondéré, opportunités gagnées ou perdues.", "all"),
                ("bi-graph-up", "Prévisions de ventes",
                 "Prévision des 6 prochains mois, pondérée par la probabilité et l'échéance.", "all"),
                ("bi-trophy", "Statistiques d'équipe",
                 "Taux de réussite à 90 et 360 jours, taux de conversion, panier moyen sur 12 mois.", "all"),
                ("bi-binoculars", "Prospection automatique",
                 "Veille sur les sites et flux de votre choix pour détecter de nouvelles opportunités.",
                 "premium"),
            ]),
        ],
        "form_hint": "Décrivez : taille de l'équipe commerciale, cycle de vente, suivi actuel des prospects…",
    },

    # ------------------------------------------------------------------ GRH
    "grh": {
        "url_name": "presentation:details_grh",
        "name": "GRH",
        "icon": "bi-person-badge",
        "plan": "all",
        "summary": (
            "Dossier salarié complet, contrats et échéances, congés, avances, retenues, prêts "
            "et fin de contrat."
        ),
        "lead": (
            "Centralisez les dossiers de vos salariés, de l'embauche à la sortie : contrats, période "
            "d'essai, congés, avances et prêts, fin de contrat avec indemnités et certificat de travail."
        ),
        "badges": ["Dossier salarié", "Alertes contrats"],
        "headline": "Vos salariés suivis de l'embauche à la sortie",
        "subtitle": (
            "Les informations saisies en GRH alimentent directement la paie : salaire de base, "
            "sursalaire, primes, avances et prêts."
        ),
        "steps": [
            ("Dossier salarié", "Identité, pièce d'identité, filiation, situation familiale, contact "
             "d'urgence, n° CNPS."),
            ("Contrat", "Type de contrat, catégorie, fonction, salaire de base, sursalaire, primes et "
             "allocations, période d'essai."),
            ("Congés", "Demandes de congé, état des congés et attestation de congé."),
            ("Avances, retenues & prêts", "Échéancier déduit automatiquement des bulletins de paie."),
            ("Fin de contrat", "Motif, indemnités de fin de contrat, certificat de travail, réactivation."),
        ],
        "tabs": [
            ("Dossier & contrats", [
                ("bi-person-vcard", "Dossier salarié",
                 "État civil, pièce d'identité, filiation, enfants à charge, contact d'urgence, n° CNPS.", "all"),
                ("bi-file-earmark-text", "Contrats",
                 "CDI, CDD…, période d'essai et renouvellement, catégorie socio-professionnelle.", "all"),
                ("bi-bell", "Contrats échus ou à échoir",
                 "Alerte sur l'accueil et liste des contrats arrivant à échéance.", "all"),
                ("bi-box-arrow-right", "Fin de contrat",
                 "Motif de sortie, indemnités de fin de contrat, certificat de travail, réactivation.", "all"),
            ]),
            ("Congés, avances & prêts", [
                ("bi-calendar2-week", "Congés",
                 "Demandes, état des congés, attestation, avertissement si les jours dépassent les droits "
                 "acquis.", "all"),
                ("bi-calculator", "Calcul du congé payé",
                 "Estimation de l'allocation de congé, même avant l'établissement du bulletin.", "paid"),
                ("bi-cash", "Avances & retenues",
                 "Avances sur salaire et retenues diverses, reprises sur les bulletins.", "all"),
                ("bi-bank2", "Prêts",
                 "Montant, nombre d'échéances, échéance courante et progression du remboursement.", "all"),
            ]),
        ],
        "form_hint": "Décrivez : effectif, types de contrats, gestion actuelle des congés et des prêts…",
    },

    # ------------------------------------------------------------------ Paie
    "paie": {
        "url_name": "presentation:details_paies",
        "name": "Paie",
        "icon": "bi-cash-coin",
        "plan": "all",
        "summary": (
            "Bulletins automatiques ou manuels conformes à la législation ivoirienne (ITS, CNPS, CMU), "
            "états de paie, État 301, DISA et comptabilisation."
        ),
        "lead": (
            "Calculez vos bulletins selon la réglementation ivoirienne : ITS, CNPS, CMU, prime "
            "d'ancienneté, sursalaire, avances et prêts. Éditez les bulletins, les états annuels "
            "(État 301, DISA) et comptabilisez la paie."
        ),
        "badges": ["ITS • CNPS • CMU", "État 301 & DISA"],
        "headline": "Une paie juste, calculée et comptabilisée",
        "subtitle": (
            "Les éléments du contrat (GRH) et vos paramètres de paie suffisent : Fincompta calcule le "
            "brut, les retenues fiscales et sociales, les charges patronales et le net à payer."
        ),
        "steps": [
            ("Paramètres de paie", "Taux et barèmes, taux AT CNPS employeur, rubriques de primes."),
            ("Calcul", "Paie automatique selon les paramètres, ou assistant de paie manuelle pas à pas."),
            ("Validation", "Contrôle et validation des bulletins ; paie groupée pour valider en lot."),
            ("États", "Bulletins PDF, état de la paie par mois et par exercice, État 301, DISA."),
            ("Comptabilisation", "Écriture de paie générée par bulletin ou pour tout le mois."),
        ],
        "tabs": [
            ("Calcul des bulletins", [
                ("bi-lightning-charge", "Paie automatique",
                 "Bulletin calculé selon le contrat et les paramètres : brut, ITS, CNPS, CMU, net à payer.",
                 "all"),
                ("bi-ui-checks", "Paie manuelle",
                 "Assistant pas à pas pour ajuster jours travaillés, primes et retenues.", "all"),
                ("bi-plus-slash-minus", "Éléments variables",
                 "Prime d'ancienneté calculée, sursalaire, prime de transport, gratifications, avances et "
                 "échéances de prêt.", "all"),
                ("bi-people-fill", "Paie groupée",
                 "Calcul et validation des bulletins de tous les salariés en lot.", "paid"),
            ]),
            ("États & déclarations", [
                ("bi-file-earmark-pdf", "Bulletins de paie",
                 "Bulletins PDF avec parts salariale et patronale.", "all"),
                ("bi-table", "État de la paie",
                 "Par mois et par exercice, avec totaux des gains, retenues et charges.", "all"),
                ("bi-file-earmark-spreadsheet", "État 301 & DISA",
                 "Synthèse annuelle par salarié et déclaration individuelle des salaires annuels.", "all"),
                ("bi-journal-check", "Comptabilisation",
                 "Par bulletin, ou « Tout comptabiliser » pour le mois entier (Starter & Premium).", "all"),
            ]),
            ("Simulateurs", [
                ("bi-calculator", "Simulateur de salaire",
                 "Partez d'un salaire net visé pour obtenir le brut et le coût employeur.", "paid"),
                ("bi-sliders", "Simulateur de sursalaire",
                 "Simulez un nouveau sursalaire par employé et comparez avec la situation actuelle.", "paid"),
            ]),
        ],
        "form_hint": "Décrivez : effectif, primes et avantages, périodicité, déclarations à produire…",
    },

    # ------------------------------------------------------------------ États financiers
    "etats": {
        "url_name": "presentation:details_etats_financiers",
        "name": "États & Analyses",
        "icon": "bi-graph-up",
        "plan": "all",
        "summary": (
            "Balance générale, grand livre tiers, compte d'exploitation, comparatifs N / N-1 / N-2, "
            "clôture d'exercice et analyses financières."
        ),
        "lead": (
            "Obtenez vos états à tout moment depuis la comptabilité : balance, grand livre tiers, "
            "compte d'exploitation, tableau de bord comparatif et, en Premium, l'analyse financière "
            "complète (ratios, bilan fonctionnel, FRNG, BFR, trésorerie nette)."
        ),
        "badges": ["Comparatifs N / N-1 / N-2", "Exports PDF"],
        "headline": "Des états toujours à jour, des indicateurs pour décider",
        "subtitle": (
            "Pas d'extraction ni de tableur : les états sont calculés en direct à partir des écritures "
            "et comparés aux exercices précédents."
        ),
        "steps": [
            ("Tableau de bord", "Indicateurs clés de l'exercice comparés à la même période N-1, CA mensuel "
             "N vs N-1, alertes."),
            ("États comptables", "Balance générale, détail d'un compte, grand livre tiers, compte "
             "d'exploitation."),
            ("États sociaux", "État 301 et DISA établis à partir de la paie."),
            ("Analyses", "Marges, délais clients et fournisseurs, liquidité, bilan fonctionnel (Premium)."),
            ("Clôture", "Clôture de l'exercice et génération des reports à nouveau."),
        ],
        "tabs": [
            ("États comptables", [
                ("bi-list-check", "Balance générale",
                 "Par période, avec le détail de chaque compte et export PDF.", "all"),
                ("bi-people", "Grand livre tiers",
                 "Balance et détail des comptes clients et fournisseurs, export PDF.", "all"),
                ("bi-bar-chart-steps", "Compte d'exploitation",
                 "Chiffre d'affaires, EBE, résultat d'exploitation et financier, avec le détail par compte.",
                 "all"),
                ("bi-lock", "Clôture d'exercice",
                 "Clôture, résultat net et lignes à nouveau générées pour l'exercice suivant.", "all"),
            ]),
            ("Pilotage", [
                ("bi-speedometer2", "Tableau de bord comparatif",
                 "Indicateurs N à date vs N-1 même période, CA mensuel N vs N-1, compte de résultat N-1 et "
                 "N-2.", "all"),
                ("bi-file-earmark-spreadsheet", "État 301 & DISA",
                 "États sociaux annuels issus de la paie.", "all"),
                ("bi-graph-up-arrow", "Analyses financières",
                 "Marges brute et d'exploitation, délais clients et fournisseurs, liquidités, trésorerie "
                 "nette mois par mois.", "premium"),
                ("bi-diagram-3", "Structures financières",
                 "Bilan fonctionnel, FRNG, BFRE/BFRHE, trésorerie nette, autonomie financière, rentabilité, "
                 "capacité de remboursement.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : états attendus, fréquence de reporting, exercices à comparer…",
    },

    # ------------------------------------------------------------------ Budget
    "budget": {
        "url_name": "presentation:details_budget",
        "name": "Gestion budgétaire",
        "icon": "bi-pie-chart",
        "plan": "premium",
        "summary": (
            "Rubriques et lignes budgétaires, saisie mensuelle ou annuelle, suivi budget vs réalisé "
            "lu dans la comptabilité, exports Excel."
        ),
        "lead": (
            "Construisez votre budget par rubriques et lignes, rattachez chaque ligne à ses comptes "
            "comptables et suivez chaque mois le réalisé, les écarts et le taux de consommation, "
            "sans aucune ressaisie."
        ),
        "badges": ["Budget vs réalisé", "Exports Excel"],
        "headline": "Un budget suivi en temps réel depuis la comptabilité",
        "subtitle": (
            "Le réalisé est lu directement dans les écritures : dès qu'une dépense est comptabilisée, "
            "elle apparaît dans le suivi budgétaire."
        ),
        "steps": [
            ("Paramétrage", "Rubriques et lignes budgétaires (nature fixe ou variable, responsable)."),
            ("Règles comptables", "Chaque ligne est rattachée à un compte exact, un préfixe ou une plage "
             "de comptes."),
            ("Saisie du budget", "Mois par mois, ou montant annuel réparti automatiquement sur 12 mois."),
            ("Validation", "Budget en brouillon, validé puis clôturé."),
            ("Suivi", "Budget, réalisé, écart et consommation, par mois et sur l'année, avec alertes."),
        ],
        "tabs": [
            ("Construction", [
                ("bi-diagram-2", "Rubriques & lignes",
                 "Organisation du budget par rubriques, lignes activables/désactivables, responsable.",
                 "premium"),
                ("bi-link", "Règles comptables",
                 "Rattachement par compte exact, préfixe ou plage : le réalisé se calcule tout seul.",
                 "premium"),
                ("bi-calendar3", "Saisie mensuelle ou annuelle",
                 "Saisie sur un mois ou sur les 12 mois, avec répartition d'un montant annuel.", "premium"),
            ]),
            ("Suivi", [
                ("bi-bar-chart", "Suivi mensuel",
                 "Budget du mois et cumulé, réalisé, écart et alertes de dépassement.", "premium"),
                ("bi-calendar-range", "Synthèse annuelle",
                 "Consommation annuelle par ligne et par rubrique.", "premium"),
                ("bi-file-earmark-excel", "Exports Excel",
                 "Export de la saisie annuelle et des suivis mensuel et annuel.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : structure de votre budget, nombre de lignes, fréquence du suivi…",
    },

    # ------------------------------------------------------------------ Audit
    "audit": {
        "url_name": "presentation:details_audit",
        "name": "Audit comptable",
        "icon": "bi-clipboard-check",
        "plan": "paid",
        "summary": (
            "14 contrôles automatiques de la comptabilité, justification des anomalies et checklist "
            "de révision."
        ),
        "lead": (
            "Faites réviser votre comptabilité en continu : Fincompta passe vos écritures au crible de "
            "14 contrôles, liste les anomalies à corriger ou justifier et vous guide avec une checklist "
            "de révision avant la clôture."
        ),
        "badges": ["14 contrôles automatiques", "Checklist de révision"],
        "headline": "Une comptabilité révisée avant la clôture",
        "subtitle": (
            "Déséquilibres, doublons, comptes d'attente non soldés, cut-off, amortissements… les "
            "anomalies sont détectées avant qu'elles ne faussent vos états."
        ),
        "steps": [
            ("Lancer les contrôles", "Sur l'exercice de votre choix, à la demande."),
            ("Anomalies", "Chaque anomalie est classée par contrôle et par niveau de gravité."),
            ("Correction ou justification", "Corrigez l'écriture en cause ou justifiez l'anomalie."),
            ("Checklist", "Suivez les points de révision jusqu'à la clôture."),
        ],
        "tabs": [
            ("Contrôles des écritures", [
                ("bi-arrow-left-right", "Équilibre & montants",
                 "Écritures déséquilibrées, lignes sans montant, comptes absents du plan comptable.", "paid"),
                ("bi-files", "Doublons & pièces",
                 "Doublons de saisie, pièces saisies plusieurs fois, collisions de références.", "paid"),
                ("bi-person-x", "Tiers",
                 "Tiers inconnu ou incohérent avec le compte (ex. : client sur un compte fournisseur).",
                 "paid"),
            ]),
            ("Contrôles de révision", [
                ("bi-hourglass-split", "Comptes d'attente",
                 "Soldes restants sur les comptes d'attente (471, 472, 475) et de virements internes (58).",
                 "paid"),
                ("bi-building-gear", "Immobilisations",
                 "Dotations sans immobilisation, immobilisations non amorties, crédit-bail à retraiter.",
                 "paid"),
                ("bi-calendar-x", "Cut-off",
                 "Montants anormalement élevés sur le mois de clôture pour les comptes de charges et "
                 "produits.", "paid"),
                ("bi-list-task", "Checklist de révision",
                 "Points de révision à cocher, avec le détail des anomalies associées.", "paid"),
            ]),
        ],
        "form_hint": "Décrivez : volume d'écritures, calendrier de clôture, intervention d'un cabinet…",
    },

    # ------------------------------------------------------------------ Prospection
    "prospection": {
        "url_name": "presentation:details_prospection",
        "name": "Prospection",
        "icon": "bi-binoculars",
        "plan": "premium",
        "summary": (
            "Veille automatique sur les sites et flux RSS de votre choix, filtrée par vos mots-clés "
            "et classée par pertinence."
        ),
        "lead": (
            "Ne ratez plus une opportunité : Fincompta surveille les sites et flux que vous choisissez "
            "(appels d'offres, annonces, actualités de votre secteur), repère vos mots-clés et classe "
            "les résultats par pertinence."
        ),
        "badges": ["Veille automatique", "Sources & mots-clés"],
        "headline": "Vos opportunités détectées automatiquement",
        "subtitle": (
            "La prospection complète le CRM : les résultats pertinents deviennent des prospects et "
            "des opportunités."
        ),
        "steps": [
            ("Sources", "Ajoutez les sites (flux RSS/Atom ou pages HTML) à surveiller et leur poids."),
            ("Mots-clés", "Définissez les mots-clés propres à votre activité."),
            ("Collecte", "Recherches automatiques ou lancées à la demande."),
            ("Résultats", "Articles classés par score : mots-clés trouvés, présence dans le titre, poids "
             "de la source."),
        ],
        "tabs": [
            ("Veille", [
                ("bi-rss", "Sources",
                 "Sites et flux RSS/Atom ou HTML, activables à volonté, pondérés dans le classement.",
                 "premium"),
                ("bi-key", "Mots-clés",
                 "Liste de mots-clés propre à votre organisation.", "premium"),
                ("bi-sort-down", "Résultats classés",
                 "Résultats triés par date et par score de pertinence.", "premium"),
                ("bi-play-circle", "Recherche à la demande",
                 "Lancez une collecte manuelle en plus des recherches automatiques.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : votre secteur, les sites à surveiller, les opportunités recherchées…",
    },

    # ------------------------------------------------------------------ Association / ONG
    "association": {
        "url_name": "presentation:details_association",
        "name": "Association / ONG",
        "icon": "bi-heart",
        "plan": "asso",
        "summary": (
            "Version dédiée aux associations, ONG, fondations et projets : plan comptable et états "
            "SYCEBNL, trésorerie, GRH, paie et audit."
        ),
        "lead": (
            "Une version de Fincompta conçue pour les entités à but non lucratif : plan comptable "
            "SYCEBNL installé à l'inscription, états financiers SYCEBNL (bilan, tableau "
            "emplois-ressources, exécution budgétaire, notes annexes), caisse, GRH, paie et un audit "
            "qui connaît les règles propres aux fonds dédiés, subventions et contributions en nature."
        ),
        "badges": ["Conforme SYCEBNL", "États SYCEBNL"],
        "headline": "La comptabilité SYCEBNL, sans tableur",
        "subtitle": (
            "Cotisations, dons, subventions, fonds affectés à des projets : vos opérations sont "
            "saisies une fois et vos états SYCEBNL sont produits directement."
        ),
        "steps": [
            ("Paramétrage", "Plan comptable SYCEBNL, journaux et paramètres de paie installés à la "
             "création du compte."),
            ("Saisie", "Opérations, caisse, écritures récurrentes et import Excel des écritures."),
            ("Paie", "Bulletins conformes (ITS, CNPS, CMU), État 301, DISA, comptabilisation."),
            ("Audit", "23 contrôles automatiques, dont 9 propres au SYCEBNL."),
            ("États & clôture", "Bilan, compte d'exploitation, emplois-ressources, exécution budgétaire, "
             "notes annexes, clôture."),
        ],
        "tabs": [
            ("États SYCEBNL", [
                ("bi-building", "Bilan",
                 "Actif / passif avec comparatif N-1 : dotations, fonds propres, fonds affectés et reportés, "
                 "fonds de projet, excédent ou déficit.", "asso"),
                ("bi-arrow-down-up", "Tableau emplois-ressources",
                 "Pour les projets : ressources, immobilisations, charges de fonctionnement, excédent ou "
                 "déficit des fonds reçus et contrôle de la trésorerie.", "asso"),
                ("bi-clipboard-data", "Exécution budgétaire",
                 "Budget, décaissements, engagements, réalisation, crédit disponible et taux d'exécution "
                 "par ligne.", "asso"),
                ("bi-journal-bookmark", "Notes annexes",
                 "Contributions volontaires en nature (classe 9), legs, dons et usufruits temporaires.", "asso"),
            ]),
            ("Audit SYCEBNL", [
                ("bi-arrow-repeat", "Reprises de fonds",
                 "Subventions d'investissement, fonds de dons et legs, fonds affectés aux projets non repris.",
                 "asso"),
                ("bi-cash-coin", "Dotations & fonds d'administration",
                 "Dotation consomptible non transférée, fonds d'administration (462 / 702), apports non "
                 "libérés.", "asso"),
                ("bi-people", "Adhérents & usagers",
                 "Cotisations et ventes passées sur le bon compte (adhérents 411, clients-usagers 412).",
                 "asso"),
                ("bi-gift", "Contributions en nature & usufruit",
                 "Contributions volontaires hors classe 9, usufruit temporaire non amorti.", "asso"),
            ]),
            ("Modules inclus", [
                ("bi-journal-text", "Comptabilité & caisse",
                 "Saisie, import Excel des écritures, écritures récurrentes, lettrage, recherche, journal "
                 "de caisse.", "asso"),
                ("bi-person-badge", "GRH & Paie",
                 "Dossiers salariés, contrats, congés, prêts, bulletins, paie groupée, simulateurs, État 301, "
                 "DISA.", "asso"),
                ("bi-graph-up", "Analyses",
                 "Balance, grand livre tiers, compte d'exploitation, analyses et structures financières.",
                 "asso"),
                ("bi-clipboard-check", "Audit comptable",
                 "Les 14 contrôles de la version entreprise, plus 9 contrôles SYCEBNL et la checklist de "
                 "révision.", "asso"),
            ]),
        ],
        "form_hint": "Décrivez : type d'entité, projets et bailleurs, nombre de salariés, états à produire…",
    },
}

# Ordre d'affichage (accueil, pied de page, navigation entre modules).
MODULE_ORDER = [
    "comptabilite", "tresorerie", "facturation", "crm", "grh", "paie",
    "etats", "budget", "audit", "prospection",
]

for _slug, _module in MODULES.items():
    _module["slug"] = _slug
    _module["plan_label"] = PLAN_LABELS[_module["plan"]]
    _module["plans_text"] = PLAN_AVAILABILITY[_module["plan"]]
    _module["asso_note"] = ASSO_AVAILABILITY.get(_slug)
    _module["tabs"] = [
        {
            "title": title,
            "features": [
                {"icon": icon, "title": ftitle, "text": text, "plan": plan,
                 "plan_label": PLAN_LABELS[plan]}
                for icon, ftitle, text, plan in features
            ],
        }
        for title, features in _module["tabs"]
    ]
    _module["steps"] = [{"title": t, "text": d} for t, d in _module["steps"]]


def module_list():
    return [MODULES[slug] for slug in MODULE_ORDER]


# Comparatif des formules affiché sur l'accueil : Free, Starter, Premium
# (fincompta) puis Association/ONG (syscebnl).
# Valeurs : True (inclus), False (non inclus) ou texte.
PLAN_COMPARISON = [
    ("Utilisateurs", "1", "2", "10", "10"),
    ("Salariés gérés (GRH & Paie)", "2", "20", "200", "200"),
    ("Référentiel comptable", "SYSCOHADA révisé", "SYSCOHADA révisé", "SYSCOHADA révisé", "SYCEBNL"),
    ("Comptabilité : saisie, lettrage, recherche", True, True, True, True),
    ("Journal de caisse", True, True, True, True),
    ("État de caisse & rapport mensuel par e-mail", True, True, True, False),
    ("Facturation & CRM", True, True, True, False),
    ("GRH & Paie (bulletins, État 301, DISA)", True, True, True, True),
    ("Balance, grand livre tiers, compte d'exploitation", True, True, True, True),
    ("Bilan, emplois-ressources, exécution budgétaire, notes annexes", False, False, False, True),
    ("Import des écritures (Excel) & écritures récurrentes", False, True, True, True),
    ("Import des ventes E-impôt", False, True, True, False),
    ("Paie groupée, simulateurs, calcul du congé payé", False, True, True, True),
    ("Comptabilisation de la paie du mois en un clic", False, True, True, False),
    ("Audit comptable", False, "14 contrôles", "14 contrôles", "23 contrôles"),
    ("Analyses financières & structures financières", False, False, True, True),
    ("Gestion budgétaire", False, False, True, False),
    ("Prospection automatique", False, False, True, False),
    ("Support", "Standard", "Standard", "Prioritaire", "Standard"),
]


def plan_comparison():
    return [{"label": row[0], "values": row[1:]} for row in PLAN_COMPARISON]
