import pandas as pd


def audit_stations():
    """
    Analyse le fichier stations.csv.

    Vérifie :
    - Le nombre de stations.
    - Les doublons d'identifiants.
    - Les valeurs manquantes.
    - Les capacités nulles ou négatives.
    - Le format des identifiants de station.

    Retourne le DataFrame pour les contrôles des trajets.
    """

    stations = pd.read_csv("data/stations.csv")

    print("\n========== AUDIT STATIONS ==========")

    print(f"Nombre de stations : {len(stations)}")

    print(f"Doublons station_id : " f"{stations['station_id'].duplicated().sum()}")

    print(f"Valeurs manquantes :\n{stations.isna().sum()}")

    print(f"Capacités <= 0 : " f"{(stations['capacite'] <= 0).sum()}")

    print(
        f"Identifiants au format invalide : "
        f"{(~stations['station_id'].str.fullmatch(r'S\d{3}')).sum()}"
    )

    return stations


def audit_trajets(stations):
    """
    Analyse le fichier trajets.csv.

    Vérifie :
    - Le nombre de trajets.
    - Les doublons d'identifiants et les doublons exacts.
    - Les valeurs manquantes.
    - La cohérence du type d'usager avec sa référence.
    - Les durées nulles ou négatives.
    - L'existence des stations de départ et d'arrivée.
    """

    trajets = pd.read_csv("data/trajets.csv")

    print("\n========== AUDIT TRAJETS ==========")

    # Contrôles généraux
    print(f"Nombre de trajets : {len(trajets)}")

    print(f"Doublons trajet_id : " f"{trajets['trajet_id'].duplicated().sum()}")

    print(f"Valeurs manquantes :\n{trajets.isna().sum()}")

    print(f"Doublons de lignes complètes : " f"{trajets.duplicated().sum()}")

    # RG5 : cohérence des références d'usagers
    print(
        f"Abonnés sans usager_ref : "
        f"{((trajets['type_usager'] == 'abonne') & trajets['usager_ref'].isna()).sum()}"
    )

    print(
        f"Occasionnels avec usager_ref : "
        f"{((trajets['type_usager'] == 'occasionnel') & trajets['usager_ref'].notna()).sum()}"
    )

    # RG4 : durée strictement positive
    print(f"Durées <= 0 : " f"{(trajets['duree_secondes'] <= 0).sum()}")

    # RG2 : les stations de départ doivent exister
    print(
        f"Stations de départ inconnues : "
        f"{(~trajets['station_depart'].isin(stations['station_id'])).sum()}"
    )

    # RG2 / RG3 : arrivée absente autorisée, mais pas inconnue
    print(
        f"Stations d'arrivée inconnues : "
        f"{((trajets['station_arrivee'].notna()) & (~trajets['station_arrivee'].isin(stations['station_id']))).sum()}"
    )


def audit_incidents():
    """
    Analyse le fichier incidents.csv.

    Vérifie :
    - Le nombre d'incidents et les doublons.
    - Les valeurs manquantes.
    - La cohérence cible / identifiants (RG6).
    - Les valeurs autorisées des statuts.
    - La cohérence entre statut et date de résolution (RG8).
    - L'ordre chronologique des dates.

    Normalise les statuts et convertit les dates en mémoire.
    """

    incidents = pd.read_csv("data/incidents.csv")

    print("\n========== AUDIT INCIDENTS ==========")

    # 1. Contrôles généraux
    print(f"Nombre d'incidents : {len(incidents)}")

    print(f"Doublons incident_id : " f"{incidents['incident_id'].duplicated().sum()}")

    print(f"Valeurs manquantes :\n{incidents.isna().sum()}")

    # 2. RG6 : cohérence entre la cible et les identifiants
    print("\n--- RG6 : Cible des incidents ---")

    print(
        f"Incidents de station avec velo_id : "
        f"{((incidents['cible'] == 'station') & incidents['velo_id'].notna()).sum()}"
    )

    print(
        f"Incidents de station sans station_id : "
        f"{((incidents['cible'] == 'station') & incidents['station_id'].isna()).sum()}"
    )

    print(
        f"Incidents de vélo sans velo_id : "
        f"{((incidents['cible'] == 'velo') & incidents['velo_id'].isna()).sum()}"
    )

    print(
        f"Incidents de vélo avec station_id : "
        f"{((incidents['cible'] == 'velo') & incidents['station_id'].notna()).sum()}"
    )

    print(
        f"fzfzefzefzfzfezfzfzfzfzfzefzfzfzefzefzefzefzfe{(~incidents['cible'].isin(['velo','station'])).sum()}"
    )

    # 3. Normalisation des statuts AVANT les contrôles RG8
    print("\n--- Normalisation des statuts ---")

    incidents["statut"] = incidents["statut"].str.lower()
    incidents["statut"] = incidents["statut"].replace("en cours", "en_cours")

    print(
        f"Statuts non autorisés : "
        f"{(~incidents['statut'].isin(['ouvert', 'en_cours', 'resolu'])).sum()}"
    )

    print(f"Statuts présents :\n{incidents['statut'].drop_duplicates()}")

    # 4. Conversion des dates
    incidents["date_signalement"] = pd.to_datetime(incidents["date_signalement"])

    incidents["date_resolution"] = pd.to_datetime(incidents["date_resolution"])

    # 5. RG8 : cohérence des dates et des statuts
    print("\n--- RG8 : Dates de résolution ---")

    print(
        f"Incidents résolus sans date de résolution : "
        f"{((incidents['statut'] == 'resolu') & incidents['date_resolution'].isna()).sum()}"
    )

    print(
        f"Incidents ouverts ou en cours avec date de résolution : "
        f"{(((incidents['statut'] == 'ouvert') | (incidents['statut'] == 'en_cours')) & incidents['date_resolution'].notna()).sum()}"
    )

    dates_invalides = incidents["date_resolution"] < incidents["date_signalement"]

    print(
        f"Dates de résolution antérieures au signalement : " f"{dates_invalides.sum()}"
    )

    print("\nIncidents concernés :")
    print(incidents[dates_invalides])


def main():
    """
    Exécute les audits des trois fichiers CSV dans l'ordre.
    """

    stations = audit_stations()
    audit_trajets(stations)
    audit_incidents()


if __name__ == "__main__":
    main()
