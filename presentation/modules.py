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
    "tresorerie": "Journal de caisse inclus. Sans banque, rapprochement ni prévisionnel, ni état de "
                  "caisse et rapport mensuel par e-mail.",
    "facturation_crm": None,
    "grh": "Inclus.",
    "paie": "Inclus. Comptabilisation bulletin par bulletin.",
    "etats": "Inclus, avec en plus les états SYCEBNL : bilan, tableau emplois-ressources, "
             "exécution budgétaire et notes annexes.",
    "cdg": None,
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
            ("Axe analytique", [
                ("bi-diagram-3", "Centre à la saisie",
                 "Charges et produits affectés à un centre de responsabilité dès la saisie, à la caisse et à "
                 "la comptabilisation des factures et de la paie.", "premium"),
                ("bi-kanban", "Rattachement aux projets",
                 "Une écriture peut être rattachée à un ou plusieurs projets, en tout ou en partie, sans "
                 "modifier la comptabilité.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : volume d'écritures, journaux, imports à prévoir, reprise d'historique…",
    },

    # ------------------------------------------------------------------ Trésorerie
    "tresorerie": {
        "url_name": "presentation:details_tresorerie",
        "name": "Gestion de trésorerie",
        "icon": "bi-cash-coin",
        "plan": "all",
        "summary": (
            "Caisse et banque, comptes de trésorerie, virements internes, rapprochement bancaire "
            "avec import des relevés, prévisionnel de trésorerie et rapport mensuel par e-mail."
        ),
        "lead": (
            "Tenez la caisse et la banque au jour le jour, rapprochez vos relevés bancaires en quelques "
            "clics et anticipez vos besoins : la position consolidée et le prévisionnel sont calculés "
            "directement depuis la comptabilité, sans tableur."
        ),
        "badges": ["Caisse & banque", "Rapprochement bancaire", "Prévisionnel 13 semaines / 12 mois"],
        "headline": "Votre trésorerie lisible aujourd'hui, anticipée pour demain",
        "subtitle": (
            "Les soldes sont lus dans les écritures comptables : chaque opération de caisse ou de banque "
            "alimente directement les journaux, le rapprochement et le prévisionnel."
        ),
        "steps": [
            ("Comptes de trésorerie", "Banques, caisses et mobile money détectés depuis la comptabilité, "
             "avec seuil d'alerte et découvert autorisé."),
            ("Caisse & banque", "Entrées et sorties saisies avec n° de pièce, tiers, type d'opération et "
             "pièces justificatives ; écriture générée automatiquement."),
            ("Virements internes", "Caisse ↔ banque ou banque ↔ banque via le compte 585, neutres pour la "
             "trésorerie."),
            ("Rapprochement", "Import du relevé (PDF, CSV ou Excel), rapprochement automatique et manuel, "
             "frais bancaires comptabilisés depuis le relevé."),
            ("Pilotage", "Tableau de bord, prévisionnel 13 semaines / 12 mois avec scénario pessimiste, "
             "rapport mensuel du dirigeant par e-mail."),
        ],
        "tabs": [
            ("Caisse & banque", [
                ("bi-cash-stack", "Journal de caisse",
                 "Entrées et sorties par jour et par mois, avec n° de pièce, tiers, type d'opération, pièces "
                 "justificatives et bordereau imprimable.", "all"),
                ("bi-bank", "Banque",
                 "Encaissements et décaissements saisis comme à la caisse (virements, chèques, frais, agios, "
                 "salaires, CNPS…), avis d'opération PDF, alerte de découvert.", "all"),
                ("bi-tags", "Types d'opération",
                 "Chaque type d'opération de caisse ou de banque sait quels comptes mouvementer : pas de "
                 "schéma comptable à connaître.", "all"),
                ("bi-diagram-3", "Centre analytique",
                 "La charge ou le produit est affecté à un centre de responsabilité dès la saisie.",
                 "premium"),
            ]),
            ("Comptes & rapprochement", [
                ("bi-wallet2", "Comptes de trésorerie",
                 "Banques, caisses et mobile money, seuil d'alerte, découvert autorisé, journal mensuel par "
                 "compte avec solde progressif.", "paid"),
                ("bi-arrow-left-right", "Virements internes",
                 "Virements entre caisse et banques via le compte 585, suivis et neutres pour la trésorerie.",
                 "paid"),
                ("bi-file-earmark-arrow-up", "Import des relevés",
                 "Relevés PDF électroniques, CSV ou Excel, soldes repris du relevé et lignes déjà importées "
                 "écartées.", "paid"),
                ("bi-check2-square", "Rapprochement bancaire",
                 "Rapprochement automatique puis manuel, frais bancaires comptabilisés depuis le relevé, état "
                 "de rapprochement en PDF.", "paid"),
            ]),
            ("Pilotage & prévisions", [
                ("bi-speedometer2", "Tableau de bord",
                 "Position consolidée, évolution mensuelle, couverture des charges, principaux encaissements "
                 "et décaissements, alertes.", "paid"),
                ("bi-graph-up-arrow", "Prévisionnel de trésorerie",
                 "13 semaines ou 12 mois : créances clients, dettes fournisseurs, paie, TVA, abonnements, "
                 "charges courantes projetées sur leur tendance, flux saisis et scénario pessimiste.", "paid"),
                ("bi-envelope-paper", "État de caisse & rapport mensuel",
                 "État de caisse par e-mail et, chaque mois, un rapport clair : avez-vous gagné de l'argent ? "
                 "combien avez-vous ? qui vous doit ?", "all"),
                ("bi-file-earmark-arrow-down", "Exports PDF & Excel",
                 "Tableau de bord, journaux, rapprochement et prévisionnel exportés en PDF et Excel.", "paid"),
            ]),
        ],
        "form_hint": "Décrivez : nombre de caisses et de comptes bancaires, mobile money, volume "
                     "d'opérations, besoin de prévisions…",
    },

    # ------------------------------------------------------------------ Facturation & CRM
    "facturation_crm": {
        "url_name": "presentation:detail_facturation_crm",
        "name": "Facturation & CRM",
        "icon": "bi-receipt",
        "plan": "all",
        "summary": (
            "Clients et prospects, activités, pipeline Kanban et prévisions ; devis et factures avec "
            "QR code, envoi par e-mail, paiements partiels et comptabilisation en un clic."
        ),
        "lead": (
            "Suivez vos clients et prospects, faites avancer les opportunités dans le pipeline, puis "
            "émettez devis et factures, suivez les règlements et les impayés et comptabilisez chaque "
            "facture sans ressaisie : de la première activité commerciale à l'encaissement."
        ),
        "badges": ["Pipeline Kanban", "Devis & factures", "QR code d'authenticité"],
        "headline": "De la prospection à l'encaissement, sans ressaisie",
        "subtitle": (
            "Une fiche client unique, partagée avec la comptabilité : opportunités, devis, factures, "
            "règlements et historique des échanges sont au même endroit."
        ),
        "steps": [
            ("Clients & prospects", "Fiche entreprise (RCCM, n° de compte contribuable, contacts), "
             "commune au CRM, à la facturation et à la comptabilité."),
            ("Activités & opportunités", "Appels, rendez-vous, relances ; opportunités avec montant, "
             "probabilité et échéance, suivies dans le pipeline Kanban."),
            ("Devis & facture", "Lignes de prestation, remise, TVA et autres taxes ; conversion du devis "
             "en facture, échéance et modalité de paiement."),
            ("Envoi & encaissement", "PDF avec QR code envoyé par e-mail, règlements partiels et reste dû "
             "suivis."),
            ("Comptabilisation", "La facture passe en comptabilité en un clic, avec le choix du centre "
             "analytique en Premium."),
        ],
        "tabs": [
            ("Clients & activités", [
                ("bi-building", "Clients & prospects",
                 "Fiche entreprise, timeline des échanges, factures et synthèse par client.", "all"),
                ("bi-calendar-check", "Activités & tâches",
                 "Mes activités, toutes les activités de l'équipe, tâches assignées et échéances.", "all"),
                ("bi-cart-check", "Ventes",
                 "Ventes par client et par commercial, reste dû échu et retard maximum.", "all"),
                ("bi-binoculars", "Prospection automatique",
                 "Signaux de la veille commerciale (appels d'offres, financements…) convertis en prospects et "
                 "opportunités.",
                 "premium"),
            ]),
            ("Opportunités & prévisions", [
                ("bi-kanban", "Pipeline Kanban",
                 "Étapes du pipeline, probabilité, montant pondéré, opportunités gagnées ou perdues (avec "
                 "la raison).", "all"),
                ("bi-graph-up", "Prévisions de ventes",
                 "Prévision des 6 prochains mois, pondérée par la probabilité et l'échéance.", "all"),
                ("bi-trophy", "Statistiques d'équipe",
                 "Taux de réussite à 90 et 360 jours, taux de conversion, panier moyen sur 12 mois.", "all"),
                ("bi-speedometer2", "Tableau de bord",
                 "CA HT, TVA et TTC du mois et de l'année, CA N / N-1, top clients, opportunités ouvertes.",
                 "all"),
            ]),
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
            ("Encaissement & exports", [
                ("bi-wallet2", "Paiements partiels",
                 "Plusieurs règlements par facture, montant déjà réglé et reste dû toujours à jour.", "all"),
                ("bi-exclamation-triangle", "Factures échues",
                 "Factures échues et non payées par ancienneté, avec le retard et le reste dû par client.",
                 "all"),
                ("bi-file-earmark-arrow-down", "Rapports & exports PDF / Excel",
                 "Rapport mensuel PDF ; factures, devis, clients, opportunités, pipeline, prévisions, "
                 "activités et tâches exportés avec vos filtres.", "all"),
                ("bi-diagram-3", "Ventes par centre",
                 "À la comptabilisation, la vente est affectée au centre de responsabilité de votre choix.",
                 "premium"),
            ]),
        ],
        "form_hint": "Décrivez : équipe commerciale, cycle de vente, nombre de factures par mois, taxes "
                     "appliquées…",
    },

    # ------------------------------------------------------------------ GRH
    "grh": {
        "url_name": "presentation:details_grh",
        "name": "GRH",
        "icon": "bi-person-badge",
        "plan": "all",
        "summary": (
            "Dossier salarié complet, contrats et échéances, congés, avances, retenues, prêts, "
            "fin de contrat, État 301, DISA et exports PDF / Excel."
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
            ("États annuels", "État 301 et DISA, tableau de bord RH et situation des contrats, en PDF et "
             "Excel."),
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
            ("États & exports", [
                ("bi-file-earmark-spreadsheet", "État 301 & DISA",
                 "Synthèse annuelle par salarié et déclaration individuelle des salaires annuels, en PDF et "
                 "Excel.", "all"),
                ("bi-speedometer2", "Tableau de bord RH",
                 "Effectifs, répartitions, contrats échus ou à échoir et alertes Code du travail.", "all"),
                ("bi-file-earmark-arrow-down", "Exports PDF & Excel",
                 "Employés, congés, acomptes et retenues, situation des contrats : listes filtrées "
                 "complètes.", "all"),
                ("bi-filetype-pdf", "Fiche employé PDF",
                 "Identité, contacts, poste et récapitulatif du dernier contrat sur une page A4.", "all"),
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
            "états de paie en PDF et Excel, État 301, DISA et comptabilisation."
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
            ("États", "Bulletins PDF, état de la paie par mois et par exercice, tableau de bord, État 301, "
             "DISA, en PDF et Excel."),
            ("Comptabilisation", "Écriture de paie générée par bulletin ou pour tout le mois, charges "
             "affectées au centre du salarié (Premium)."),
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
                 "échéances de prêt retenues jusqu'au solde.", "all"),
                ("bi-people-fill", "Paie groupée",
                 "Calcul et validation des bulletins de tous les salariés en lot.", "paid"),
            ]),
            ("États & déclarations", [
                ("bi-file-earmark-pdf", "Bulletins de paie",
                 "Bulletins PDF avec parts salariale et patronale.", "all"),
                ("bi-table", "État de la paie",
                 "Par mois et par exercice, avec totaux des gains, retenues et charges ; tableau de bord de "
                 "la paie ; exports PDF et Excel.", "all"),
                ("bi-file-earmark-spreadsheet", "État 301 & DISA",
                 "Synthèse annuelle par salarié et déclaration individuelle des salaires annuels, en PDF et "
                 "Excel.", "all"),
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
                ("bi-graph-up-arrow", "Analyses financières",
                 "Marges brute et d'exploitation, délais clients et fournisseurs, liquidités, trésorerie "
                 "nette mois par mois.", "premium"),
                ("bi-diagram-3", "Structures financières",
                 "Bilan fonctionnel, FRNG, BFRE/BFRHE, trésorerie nette, autonomie financière, rentabilité, "
                 "capacité de remboursement.", "premium"),
                ("bi-layer-forward", "SIG & résultat de gestion",
                 "Soldes intermédiaires de gestion et seuil de rentabilité, comparés au budget dans le "
                 "Contrôle de gestion.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : états attendus, fréquence de reporting, exercices à comparer…",
    },

    # ------------------------------------------------------------------ Contrôle de gestion
    "cdg": {
        "url_name": "presentation:details_cdg",
        "name": "Contrôle de gestion",
        "icon": "bi-pie-chart",
        "plan": "premium",
        "summary": (
            "Budget des charges et des produits, versions, centres de responsabilité et axe "
            "analytique, analyse des écarts, résultat de gestion, SIG, projets et plan d'actions."
        ),
        "lead": (
            "Construisez votre budget de charges et de produits, affectez vos écritures à des centres "
            "de responsabilité et à des projets, puis suivez le réalisé lu dans la comptabilité : "
            "écarts, seuil de rentabilité, soldes intermédiaires de gestion et atterrissage de fin "
            "d'exercice, sans aucune ressaisie."
        ),
        "badges": ["Budget vs réalisé vs N-1", "Centres & projets"],
        "headline": "Piloter la performance depuis la comptabilité",
        "subtitle": (
            "Le réalisé est lu directement dans les écritures : dès qu'une charge ou un produit est "
            "comptabilisé, il alimente le suivi budgétaire, les centres, les projets et les indicateurs."
        ),
        "steps": [
            ("Paramétrage", "Rubriques et lignes de charges et de produits rattachées à leurs comptes "
             "(compte exact, préfixe ou plage), centres de responsabilité."),
            ("Budget", "Saisie mensuelle ou annuelle ; versions initiale, révisée et prévision "
             "(reforecast à partir du réalisé), avec version active."),
            ("Axe analytique", "Centre choisi à la saisie, à la caisse, à la comptabilisation des factures "
             "et de la paie, ou affecté par des règles automatiques."),
            ("Suivi", "Budget, réalisé et écart par mois, sur l'année, par centre et par projet, avec "
             "comparaison N-1 et écarts significatifs."),
            ("Résultats & actions", "Résultat de gestion, SIG, atterrissage, indicateurs et plan "
             "d'actions correctives."),
        ],
        "tabs": [
            ("Budget", [
                ("bi-diagram-2", "Rubriques & lignes",
                 "Budget des charges et des produits, lignes rattachées à un compte exact, un préfixe ou une "
                 "plage de comptes : le réalisé se calcule tout seul.", "premium"),
                ("bi-calendar3", "Saisie mensuelle ou annuelle",
                 "Saisie sur un mois ou sur les 12 mois de l'exercice dans une seule grille.", "premium"),
                ("bi-layers", "Versions budgétaires",
                 "Budget initial, révisé et prévision construite à partir du réalisé ; version active et "
                 "comparaison des versions.", "premium"),
                ("bi-file-earmark-excel", "Exports Excel",
                 "Chaque saisie, suivi et analyse s'exporte en Excel.", "premium"),
            ]),
            ("Suivi & analytique", [
                ("bi-bar-chart", "Suivi mensuel et annuel",
                 "Budget, réalisé, écart et taux de consommation, ligne par ligne et par rubrique.",
                 "premium"),
                ("bi-arrow-left-right", "Analyse des écarts",
                 "Budget / réalisé / N-1, écarts significatifs selon vos seuils, filtres par centre, "
                 "rubrique et sens.", "premium"),
                ("bi-diagram-3", "Centres de responsabilité",
                 "Centres de coût, de profit, support ou d'investissement : budget et réalisé ventilé par "
                 "centre, détail ligne par ligne.", "premium"),
                ("bi-shuffle", "Ventilation & règles d'affectation",
                 "Écritures de charges et de produits ventilées sur un ou plusieurs centres, à la saisie ou "
                 "par règles (compte, journal, tiers, libellé) ; centre par défaut de chaque salarié pour "
                 "la paie.", "premium"),
            ]),
            ("Résultats & pilotage", [
                ("bi-calculator", "Résultat de gestion",
                 "Marge sur coûts variables, seuil de rentabilité, point mort, marge et indice de sécurité, "
                 "levier opérationnel.", "premium"),
                ("bi-layer-forward", "SIG & atterrissage",
                 "Soldes intermédiaires de gestion SYSCOHADA (budget, réalisé, N-1) et prévision de fin "
                 "d'exercice.", "premium"),
                ("bi-kanban", "Projets",
                 "Budget prévu du projet, charges et produits réalisés rattachés, marge et consommation, "
                 "tous exercices confondus.", "premium"),
                ("bi-bullseye", "Indicateurs & plan d'actions",
                 "Indicateurs de pilotage avec objectifs annuels, actions correctives rattachées aux "
                 "écarts.", "premium"),
            ]),
        ],
        "form_hint": "Décrivez : structure de votre budget, centres et projets à suivre, fréquence du suivi…",
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
            "Veille commerciale automatique : appels d'offres, financements, créations d'entreprises "
            "et recrutements détectés, notés et convertis en prospects du CRM."
        ),
        "lead": (
            "Ne ratez plus une opportunité : Fincompta surveille les sites, flux RSS et recherches "
            "Google Actualités de votre choix, repère vos mots-clés, identifie la nature de chaque "
            "signal et le note de 0 à 100. Un clic suffit pour en faire un prospect et une "
            "opportunité dans le CRM."
        ),
        "badges": ["Veille automatique", "Score de pertinence 0-100", "Conversion en prospect CRM"],
        "headline": "Vos opportunités détectées, qualifiées et suivies",
        "subtitle": (
            "La prospection alimente le CRM : les signaux pertinents deviennent des prospects et des "
            "opportunités, et les clients déjà connus cités dans l'actualité sont repérés."
        ),
        "steps": [
            ("Sources", "Sites (flux RSS détecté automatiquement ou pages HTML ciblées) et recherches "
             "Google Actualités, avec leur poids et leur état de santé."),
            ("Mots-clés", "Variantes, préfixes (trésor*), poids et exclusions ; accents, casse et pluriels "
             "ignorés."),
            ("Collecte", "Recherches planifiées ou lancées à la demande, historique détaillé par source."),
            ("Analyse", "Nature du signal, organisation, contacts, montants et date limite extraits ; "
             "score expliqué et doublons fusionnés."),
            ("Exploitation", "Boîte de signaux à traiter, conversion en prospect et opportunité, "
             "récapitulatif par e-mail."),
        ],
        "tabs": [
            ("Veille", [
                ("bi-rss", "Sources",
                 "Flux RSS/Atom, pages HTML ciblées (filtre d'URL, sélecteur CSS) et recherches Google "
                 "Actualités ; dernier état et erreurs de chaque source.", "premium"),
                ("bi-key", "Mots-clés",
                 "Variantes, préfixes, poids et exclusions, propres à votre organisation.", "premium"),
                ("bi-play-circle", "Collecte planifiée ou à la demande",
                 "Collectes automatiques, collecte manuelle et recherche ponctuelle d'informations.",
                 "premium"),
                ("bi-clock-history", "Historique des collectes",
                 "Durée, sources interrogées et nouveaux signaux de chaque collecte.", "premium"),
            ]),
            ("Analyse des signaux", [
                ("bi-tags", "Nature du signal",
                 "Appel d'offres, financement, création, recrutement… identifiés automatiquement.",
                 "premium"),
                ("bi-sort-down", "Score de pertinence",
                 "Note de 0 à 100 expliquée : mots-clés trouvés, présence dans le titre, poids de la "
                 "source ; doublons entre médias fusionnés.", "premium"),
                ("bi-card-text", "Informations extraites",
                 "Organisation, e-mails, téléphones, montants, date de publication et date limite.",
                 "premium"),
                ("bi-people", "Clients & prospects cités",
                 "Les clients et prospects du CRM mentionnés dans un signal sont repérés.", "premium"),
            ]),
            ("Exploitation", [
                ("bi-inbox", "Boîte de signaux",
                 "Statuts (à traiter, à suivre, ignoré, converti), favoris, notes, filtres et actions "
                 "groupées.", "premium"),
                ("bi-person-plus", "Conversion en prospect",
                 "Un signal devient un prospect CRM avec une opportunité « Piste » et une note.", "premium"),
                ("bi-envelope", "Récapitulatif par e-mail",
                 "Synthèse des nouveaux signaux, ancienneté maximale et durée de conservation réglables.",
                 "premium"),
                ("bi-file-earmark-arrow-down", "Tableau de bord & exports",
                 "Tableau de bord de la veille et export PDF / Excel des signaux.", "premium"),
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
    "comptabilite", "tresorerie", "facturation_crm", "grh", "paie",
    "etats", "cdg", "audit", "prospection",
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
    ("Banque : saisie des encaissements et décaissements", True, True, True, False),
    ("État de caisse & rapport mensuel par e-mail", True, True, True, False),
    ("Facturation & CRM", True, True, True, False),
    ("GRH & Paie (bulletins, État 301, DISA)", True, True, True, True),
    ("Balance, grand livre tiers, compte d'exploitation", True, True, True, True),
    ("Bilan, emplois-ressources, exécution budgétaire, notes annexes", False, False, False, True),
    ("Import des écritures (Excel) & écritures récurrentes", False, True, True, True),
    ("Import des ventes E-impôt", False, True, True, False),
    ("Paie groupée, simulateurs, calcul du congé payé", False, True, True, True),
    ("Comptabilisation de la paie du mois en un clic", False, True, True, False),
    ("Trésorerie : rapprochement bancaire, virements, prévisionnel", False, True, True, False),
    ("Audit comptable", False, "14 contrôles", "14 contrôles", "23 contrôles"),
    ("Analyses financières & structures financières", False, False, True, True),
    ("Contrôle de gestion : budget, centres, projets, écarts", False, False, True, False),
    ("Prospection : veille commerciale automatique", False, False, True, False),
    ("Support", "Standard", "Standard", "Prioritaire", "Standard"),
]


def plan_comparison():
    return [{"label": row[0], "values": row[1:]} for row in PLAN_COMPARISON]
