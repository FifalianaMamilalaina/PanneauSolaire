-- =============================================================
-- Script d'initialisation de la base de données SolaireDB
-- =============================================================

-- Créer la base de données si elle n'existe pas
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'SolaireDB')
BEGIN
    CREATE DATABASE SolaireDB;
END
GO

USE SolaireDB;
GO

-- =============================================================
-- Table : appareils
-- =============================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'appareils')
BEGIN
    CREATE TABLE appareils (
        id INT PRIMARY KEY IDENTITY(1,1),
        nom VARCHAR(100) NOT NULL,
        puissance_w FLOAT NOT NULL,
        duree_h FLOAT NOT NULL,
        tranche VARCHAR(20) NOT NULL CHECK (tranche IN ('matin', 'soir', 'nuit'))
    );
END
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
IF NOT EXISTS (SELECT 1 FROM appareils)
BEGIN
    INSERT INTO appareils (nom, puissance_w, duree_h, tranche) VALUES
        ('Lampe salon', 15, 5, 'nuit'),
        ('Lampe chambre', 10, 4, 'nuit'),
        ('Ventilateur', 50, 8, 'matin'),
        ('Réfrigérateur', 100, 11, 'matin'),
        ('Télévision', 80, 3, 'nuit'),
        ('Chargeur téléphone', 10, 2, 'matin'),
        ('Radio', 15, 6, 'matin'),
        ('Lampe extérieure', 20, 2, 'soir');
END
GO
