-- Schéma de la base veloville (PostgreSQL 14+).
-- À compléter en respectant le contrat du sujet (types, clés, contraintes).
-- Le script doit être rejouable : prévoir les DROP ... IF EXISTS ou
-- CREATE TABLE IF NOT EXISTS.
-- ---------------------------------------------------------------
-- 1. Table station
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS station (
    station_id VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    capacite INTEGER NOT NULL,
    CONSTRAINT chk_capacite CHECK (capacite > 0),
    latitude NUMERIC(8, 5),
    longitude NUMERIC(8, 5),
    date_mise_en_service DATE
);

-- ---------------------------------------------------------------
-- 2. Table trajet
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS trajet (
    trajet_id VARCHAR(12) PRIMARY KEY,
    velo_id VARCHAR(8),
    depart_horodatage TIMESTAMP NOT NULL,
    station_depart VARCHAR(10) NOT NULL,
    CONSTRAINT fk_station_depart FOREIGN KEY (station_depart) REFERENCES Station(station_id),
    station_arrivee VARCHAR(10),
    CONSTRAINT fk_station_arrivee FOREIGN KEY (station_arrivee) REFERENCES Station(station_id),
    duree_secondes INTEGER NOT NULL,
    CONSTRAINT chk_duree_seconde CHECK (duree_secondes > 0),
    type_usager VARCHAR(20) NOT NULL CONSTRAINT chk_type_usager CHECK (type_usager IN ('abonne', 'occasionnel')),
    usager_ref VARCHAR(9)
);

-- ---------------------------------------------------------------
-- 3. Table incident
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS incident(
    incident_id VARCHAR(12) PRIMARY KEY,
    date_signalement TIMESTAMP NOT NULL,
    cible VARCHAR(10) NOT NULL CONSTRAINT chk_cible CHECK (cible IN ('velo', 'station')),
    velo_id VARCHAR(8),
    station_id VARCHAR (10),
    CONSTRAINT fk_station_id FOREIGN KEY (station_id) REFERENCES station(station_id),
    type_incident VARCHAR(50),
    statut VARCHAR(20) NOT NULL CONSTRAINT chk_statut CHECK (statut IN('ouvert', 'en_cours', 'resolu')),
    date_resolution TIMESTAMP,
    technicien VARCHAR (100),
    CONSTRAINT chk_incident_cible CHECK (
        (
            cible = 'velo'
            AND velo_id IS NOT NULL
            AND station_id IS NULL
        )
        OR (
            cible = 'station'
            AND station_id IS NOT NULL
            AND velo_id IS NULL
        )
    ),
    CONSTRAINT chk_incident_statut CHECK(
        (
            statut = 'resolu'
            AND date_resolution IS NOT NULL
            AND date_resolution >= date_signalement
        )
        OR(
            statut IN ('ouvert', 'en_cours')
            AND date_resolution IS NULL
        )
    )
);

-- ---------------------------------------------------------------
-- 4. Table utilisateur
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CONSTRAINT chk_role CHECK (role IN ('exploitant', 'direction'))
);

-- ---------------------------------------------------------------
-- 5. Index utiles aux filtres et aux indicateurs
-- ---------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_station_commune ON station(commune);

CREATE INDEX IF NOT EXISTS idx_trajet_depart_horodatage ON trajet(depart_horodatage);

CREATE INDEX IF NOT EXISTS idx_incident_statut_date ON incident(statut, date_signalement DESC);