-- =============================================================
-- Script d'initialisation de la base de données SolaireDB
-- Version 2 : heure_debut / heure_fin au lieu de duree_h
-- =============================================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'SolaireDB')
BEGIN
    CREATE DATABASE SolaireDB;
END
GO

USE SolaireDB;
GO

-- Supprimer l'ancienne table si elle existe (pour migration)
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'appareils')
BEGIN
    DROP TABLE appareils;
END
GO

-- =============================================================
-- Table : appareils (v2 avec heure_debut et heure_fin)
-- =============================================================
CREATE TABLE appareils (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom VARCHAR(100) NOT NULL,
    puissance_w FLOAT NOT NULL,
    heure_debut INT NOT NULL CHECK (heure_debut >= 0 AND heure_debut <= 23),
    heure_fin INT NOT NULL CHECK (heure_fin >= 0 AND heure_fin <= 23),
    tranche VARCHAR(20) NOT NULL CHECK (tranche IN ('matin', 'soir', 'nuit'))
);
GO

-- =============================================================
-- Table : resultats
-- =============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'resultats')
BEGIN
    CREATE TABLE resultats (
        id INT PRIMARY KEY IDENTITY(1,1),
        energie_jour FLOAT NOT NULL,
        energie_nuit FLOAT NOT NULL,
        batterie_wh FLOAT NOT NULL,
        panneau_w FLOAT NOT NULL,
        date_calcul DATETIME DEFAULT GETDATE()
    );
END
GO

-- =============================================================
-- Données d'exemple
-- =============================================================
INSERT INTO appareils (nom, puissance_w, heure_debut, heure_fin, tranche) VALUES
    ('Lampe salon', 15, 19, 0, 'nuit'),
    ('Lampe chambre', 10, 20, 0, 'nuit'),
    ('Ventilateur', 50, 8, 16, 'matin'),
    ('Réfrigérateur', 100, 6, 17, 'matin'),
    ('Télévision', 80, 19, 22, 'nuit'),
    ('Chargeur téléphone', 10, 10, 12, 'matin'),
    ('Radio', 15, 7, 13, 'matin'),
    ('Lampe extérieure', 20, 17, 19, 'soir');
GO
