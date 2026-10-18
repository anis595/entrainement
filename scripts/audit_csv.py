import pandas as pd

stations = pd.read_csv('data/stations.csv')

print(f" Le nombre de station est : {len(stations)}")


print(f"Le nombre de doublons est : {stations["station_id"].duplicated().sum()}")


print(f"Le nombre de valeur manquante est : \n{stations.isna().sum()}")


print(f"Le nombre de valeur inferrieur ou égale à 0 est : {(stations['capacite']<=0).sum()}")


print(f"les identifiants invalides sont {(~stations['station_id'].str.fullmatch(r'S\d{3}')).sum()}")


trajets = pd.read_csv('data/trajets.csv')


print(f" Le nombre de trajts est : {len(trajets)}")


print(f"Le nombre de doublons est : {trajets["trajet_id"].duplicated().sum()}")


print(f"Le nombre de valeur manquante est : \n{trajets.isna().sum()}")


print(f"Le nombre d'abonnée est : {((trajets['type_usager'] == 'abonne') & trajets['usager_ref'].isna()).sum()}")

print(f"Le nombres d'occacionnel est : {((trajets['type_usager'] == 'occasionnel') & ~(trajets['usager_ref'].isna())).sum()}")

print(f"Le nombres de doublons est : {trajets.duplicated().sum()}")

print(f"Le nombre de trajets avec une durée inferrieur à zéro est : {(trajets['duree_secondes'] <= 0).sum()}" )

print((~trajets['station_depart'].isin(stations['station_id'])).sum())